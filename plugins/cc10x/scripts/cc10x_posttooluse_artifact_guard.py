#!/usr/bin/env python3
"""PostToolUse workflow-artifact integrity guard.

Scope discipline (prevents the stale-artifact footgun):
- When the written file IS a workflow artifact (.cc10x/workflows/*.json,
  not *.events.jsonl), validate THAT file — this is the only case that may
  signal (exit 2) in `artifactIntegrity: block` mode. PostToolUse runs after
  the write: exit 2 feeds stderr to the model, it cannot undo the write, so a
  malformed artifact stays on disk until the model repairs it.
- For any other Edit/Write, audit the latest workflow artifact for telemetry
  but NEVER block: a malformed or legacy artifact from an old workflow must
  not veto unrelated writes elsewhere in the project.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from cc10x_hooklib import (
    load_input,
    load_mode,
    log_event,
    now_iso,
    read_latest_workflow_state,
    read_workflow_state,
    workflow_artifact_is_fresh,
    workflow_event_log_append,
    workflow_event_log_exists,
    workflows_dir,
)


REQUIRED_WORKFLOW_KEYS = (
    "workflow_uuid",
    "workflow_id",
    "workflow_type",
    "state_root",
    "phase_cursor",
    "task_ids",
    "results",
    "intent",
    "evidence",
    "quality",
    "status_history",
    "remediation_history",
)


def review_closure_reason(payload: dict) -> str | None:
    """Return a blocking reason when the artifact claims more review than it has.

    `planning_review_status: passed` asserts that a review read the CURRENT plan
    revision. If plan_revision has moved past last_reviewed_revision, the plan
    was amended after the review and the claim is false.

    Conditional by design: absent keys mean a legacy or half-migrated artifact,
    which MUST pass. Adding these two keys to REQUIRED_WORKFLOW_KEYS instead
    would block every artifact written before this check existed.
    """
    if payload.get("planning_review_status") != "passed":
        return None
    current = payload.get("plan_revision")
    reviewed = payload.get("last_reviewed_revision")
    if current is None or reviewed is None:
        return None  # legacy or half-migrated artifact
    # Coerce to int defensively: a hand-edited or half-migrated artifact can
    # carry "2" (string) against 2 (int). The raw `!=` would then report a
    # closure defect on values that are numerically equal, so compare the
    # coerced pair and fall back to the raw comparison when either side is
    # not coercible (a truly non-numeric revision IS a mismatch worth naming).
    try:
        current_i, reviewed_i = int(current), int(reviewed)
    except (TypeError, ValueError):
        if current != reviewed:
            return f"review-closure:plan_revision={current},last_reviewed_revision={reviewed}"
        return None
    if current_i != reviewed_i:
        return f"review-closure:plan_revision={current},last_reviewed_revision={reviewed}"
    return None


def is_workflow_artifact(path: Path) -> bool:
    if path.suffix != ".json" or path.name.endswith(".events.jsonl"):
        return False
    try:
        return path.resolve().parent == workflows_dir().resolve()
    except OSError:
        return False


_WORKFLOWS_PATH = r"\.cc10x/workflows/"
_BASH_WORKFLOW_WRITE = re.compile(
    r">>?\s*[\"']?[^\s;&|]*" + _WORKFLOWS_PATH
    + r"|\b(?:tee|cp|mv|install|touch|ln|rsync|dd|sed\s+-\S*i\S*)\b[^;&|\n]*"
    + _WORKFLOWS_PATH
    + r"|\bopen\([^)]*" + _WORKFLOWS_PATH + r"[^)]*[\"'][wax]"
)


def bash_writes_into_workflows(command: str) -> bool:
    """Heuristic, audit-only: does a Bash command write into .cc10x/workflows/?
    The router itself creates the artifact through Bash, so this never blocks."""
    return bool(_BASH_WORKFLOW_WRITE.search(command))


def main() -> int:
    data = load_input()
    mode = load_mode()
    tool_input = data.get("tool_input") or {}
    if data.get("tool_name") == "Bash":
        command = tool_input.get("command")
        if isinstance(command, str) and bash_writes_into_workflows(command):
            log_event(
                "plugin_posttooluse_bash_workflow_write",
                {
                    "wf": None,
                    "phase": "unknown",
                    "task_id": None,
                    "agent": "router",
                    "tool_name": "Bash",
                    "event": "bash_workflow_write",
                    "decision": "audit",
                    "reason": "bash-command-writes-into-workflows",
                },
            )
        return 0
    file_path = tool_input.get("file_path")
    if not file_path:
        return 0

    path = Path(file_path)
    target_is_artifact = is_workflow_artifact(path)

    if target_is_artifact:
        # Validate exactly the artifact that was just written.
        payload, artifact_path, parse_error = read_workflow_state(path.stem)
        if artifact_path is None:
            # File may have been written under a name read_workflow_state cannot
            # resolve; fall back to direct parse via latest-state helper semantics.
            payload, artifact_path, parse_error = read_latest_workflow_state()
            if artifact_path is None or artifact_path.name != path.name:
                return 0
    else:
        payload, artifact_path, parse_error = read_latest_workflow_state()
        if artifact_path is None:
            return 0

    reasons: list[str] = []
    if parse_error:
        reasons.append(f"artifact-json:{parse_error}")
    else:
        missing = [key for key in REQUIRED_WORKFLOW_KEYS if key not in payload]
        if missing:
            reasons.append("missing-keys:" + ",".join(missing))

        if not workflow_event_log_exists(payload, artifact_path):
            reasons.append("missing-event-log")

        # Value-level, not key-presence. Consequence, accepted deliberately:
        # appending here makes `reasons` non-empty, so a closure mismatch SKIPS
        # the `artifact_mutated` auto-append below. That is correct in block
        # mode — the model is told to repair the artifact, so logging a clean
        # mutation would be false — and in audit mode the reason is still
        # recorded by the log_event call further down, which runs on every
        # reason path.
        closure = review_closure_reason(payload)
        if closure:
            reasons.append(closure)

        if target_is_artifact:
            if not payload.get("updated_at"):
                reasons.append("missing-updated-at")
            elif not workflow_artifact_is_fresh(artifact_path):
                reasons.append("stale-artifact-write")

    if not reasons:
        # Fix #2: auto-append event log entry when artifact is mutated.
        # The router instructs the model to append events, but under context
        # pressure the model may skip it. This hook ensures every artifact
        # write gets a matching event log entry.
        if target_is_artifact and payload:
            wf_id = payload.get("workflow_uuid") or payload.get("workflow_id")
            if wf_id:
                workflow_event_log_append(
                    wf_id,
                    {
                        "ts": now_iso(),
                        "wf": wf_id,
                        "event": "artifact_mutated",
                        "phase": payload.get("phase_cursor", "unknown"),
                        "task_id": None,
                        "agent": "hook",
                        "decision": "auto-logged",
                        "reason": "posttool_guard_auto_append",
                    },
                )
        return 0

    decision = mode.get("artifactIntegrity", "audit")
    log_event(
        "plugin_posttooluse_artifact_guard",
        {
            "wf": (
                (payload.get("workflow_uuid") or payload.get("workflow_id"))
                if payload
                else None
            ),
            "phase": (payload or {}).get("pending_gate") or "unknown",
            "task_id": None,
            "agent": "router",
            "tool_name": data.get("tool_name"),
            "path": str(path),
            "target_is_artifact": target_is_artifact,
            "event": "posttool_artifact_guard",
            "decision": decision if target_is_artifact else "audit",
            "reason": ";".join(reasons),
        },
    )

    # Close the loop in block mode: a corrupt or key-missing artifact (the cases
    # that silently break resume/verifier handoff) must surface to the model, not
    # just the log. Exit code 2 makes Claude Code show stderr to the model; the
    # write has already happened and the file stays as written. The signal
    # applies ONLY when the write target is the artifact itself — never to
    # unrelated files — and only for hard-corruption reasons; the soft reasons (missing-event-log, stale write) stay audit-only.
    blocking_reasons = [
        r
        for r in reasons
        if r.startswith(("artifact-json:", "missing-keys:", "review-closure:"))
    ]
    if decision == "block" and target_is_artifact and blocking_reasons:
        closure_reasons = [r for r in blocking_reasons if r.startswith("review-closure:")]
        corruption = [r for r in blocking_reasons if not r.startswith("review-closure:")]
        if corruption:
            print(
                "CC10X artifact integrity guard: the workflow artifact "
                f"{artifact_path.name} is invalid ({';'.join(corruption)}). "
                "The file is already written and the malformed artifact is "
                "still on disk. Repair it now: rewrite it from "
                "references/workflow-artifact.skeleton.json before creating "
                "child tasks.",
                file=sys.stderr,
            )
        for reason in closure_reasons:
            # A message that does not say how to proceed turns a gate into a
            # wall, so both exits are named.
            print(
                "CC10X artifact integrity guard: the workflow artifact "
                f"{artifact_path.name} is inconsistent ({reason}). The file is "
                "already written and still on disk; repair it now. It claims "
                "planning_review_status=passed, but the plan was amended after the "
                "last review, so no review has read the current revision. Two ways "
                "forward: run a fresh planning review, which sets "
                "last_reviewed_revision = plan_revision, or set "
                "planning_review_status=revised_after_review to record the "
                "amendment honestly.",
                file=sys.stderr,
            )
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

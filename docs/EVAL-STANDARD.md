# CC10x Skill Eval Standard

House standard for eval-driven skill authoring in cc10x. Discipline skills (TDD,
verification-before-completion, diff-driven-docs, routing decisions) exist to make an
agent do the unglamorous thing under pressure. The only way to know a skill actually
holds under that pressure is to write the pressure down and check the behavior against it.

This standard is **not** counted by `cc10x_doc_consistency_check.py` (it lives in
`docs/`, not `plugins/cc10x/skills/`). Eval directories live as `evals/` **subdirs**
inside an individual skill dir; the doc-consistency check counts only top-level
`skills/*/` dirs, so adding `evals/` never changes the skill count.

## Why eval-driven authoring

A discipline skill is a behavioral contract, not a reference doc. Its value is measured
by whether the agent follows it **when the rationalization to skip is strongest** — small
diff, "already manually tested", obvious routing, tired at the end of a long task. Prose
alone cannot prove that. A captured pressure scenario can.

The pattern is borrowed from `superpowers:writing-skills`: every behavioral rule should
have at least one scenario where an agent WITHOUT the skill predictably fails, and the
skill is what flips that failure to a pass.

## The RED-GREEN-REFACTOR eval pattern

Each eval is one Markdown file that captures a single pressure scenario:

- **RED (the baseline failure):** What an agent does WITHOUT the skill loaded. This is the
  "Failure Signature" section. It must be a concrete, observable wrong output — not "the
  agent might be sloppy". If you cannot write a specific failure signature, the scenario is
  not exerting real pressure; cut it.
- **GREEN (the with-skill behavior):** The exact steps and output the skill forces. This is
  the "Expected Behavior (skill loaded)" section. It must be checkable: a status, a contract
  field, a command that was run, a doc that was updated.
- **REFACTOR (close the gap):** If a live run shows the agent failing even WITH the skill,
  add the agent's excuse + the counter to the skill's Rationalization Table. This is the
  "Counter" section. The eval drives skill edits; it does not just grade them.

## Required file structure (match exactly)

The canonical example is `plugins/cc10x/skills/diff-driven-docs/evals/`. New eval dirs MUST
mirror it byte-for-byte in structure and naming:

```
plugins/cc10x/skills/<skill>/evals/
  README.md                              # index: pattern recap + table of evals
  eval-01-<slug>.md
  eval-02-<slug>.md
  ...
```

Naming: `eval-NN-<kebab-slug>.md`, zero-padded, sequential from `01`. The slug names the
pressure, not the feature (e.g. `skip-temptation`, `tests-after-rationalization`).

Each `eval-NN-*.md` file MUST contain these sections, in this order:

1. `# Eval NN — <Title>`
2. `**Skill under test:** <skill id>` / `**Pressure type:** "<the rationalization>"` / a layer or scope line
3. `## Setup` — the prompt/diff/context the agent receives. Verbatim, copy-pasteable.
4. `## Pressure` — the exact rationalization the agent is told or tempted toward (a blockquote).
5. `## Expected Behavior (skill loaded)` — numbered steps ending in a checkable output, plus a bold **Key assertion** line.
6. `## Failure Signature (no skill)` — the concrete baseline failure, and one sentence on why it is wrong.
7. `## Counter (add to Rationalization Table if agent fails)` — a `| Excuse | Counter |` table feeding REFACTOR.

The `README.md` MUST recap the four-part structure and carry a table whose row count
equals the number of `eval-NN-*.md` files shipped in that dir. **Keep the table count in
sync with the files** — a README that lists more evals than it ships is the same drift bug
this standard was written to kill.

## How many evals per skill

2–4 pressure scenarios per skill. Fewer than 2 and you are not covering the distinct
rationalizations; more than 4 and you are usually re-testing the same excuse. Each scenario
must attack a **different** rationalization. If two evals share one failure signature,
merge them.

## Running an eval

Dispatch a subagent with the eval's `## Setup` + `## Pressure` as the full task, with the
skill under test loaded. Compare the agent's output against `## Expected Behavior`. A pass
matches the **Key assertion**; a fail matches the **Failure Signature** — and when it fails,
apply REFACTOR: lift the agent's actual excuse into the skill's Rationalization Table via the
eval's `## Counter` table.

These evals are author-time and review-time artifacts. They are deliberately NOT wired into
the four CI validators (harness audit, replay check, doc consistency, worldclass benchmark),
which assert literal needles and fixture contracts rather than running subagents. Evals are
run by hand or by an authoring agent when a discipline skill is created or materially changed.

## Coverage status

| Skill | Evals dir | Scenarios |
|-------|-----------|-----------|
| `diff-driven-docs` | `skills/diff-driven-docs/evals/` | 2 |
| `test-driven-development` | `skills/test-driven-development/evals/` | 3 |
| `verification-before-completion` | `skills/verification-before-completion/evals/` | 3 |
| `cc10x-router` (routing decisions) | `skills/cc10x-router/evals/` | 3 |

Highest-leverage discipline skills first. When a new discipline skill lands, add its
`evals/` dir and a row here.

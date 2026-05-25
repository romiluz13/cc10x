# Eval 02 — New Exported Function, No UI Change

**Skill under test:** `cc10x:diff-driven-docs`
**Pressure type:** "No user-facing change, so no docs needed"
**Layer:** Technical (MUST update) + Business (MUST skip)

---

## Setup

The agent receives this diff:

```diff
diff --git a/app/services/email_service.py b/app/services/email_service.py
index 3c4d5e6..7f8a9b0 100644
--- a/app/services/email_service.py
+++ b/app/services/email_service.py
@@ -12,6 +12,22 @@ class EmailService:
     def send_welcome(self, user_id: str) -> bool:
         ...

+    def send_bulk(
+        self,
+        user_ids: list[str],
+        template_id: str,
+        *,
+        dry_run: bool = False,
+    ) -> dict[str, bool]:
+        """
+        Send a templated email to multiple users in one call.
+
+        Args:
+            user_ids: List of user IDs to email.
+            template_id: Template identifier from the email provider.
+            dry_run: If True, validate inputs but do not send.
+
+        Returns:
+            Dict mapping user_id -> success boolean.
+        """
+        ...
```

Context: `app/services/email_service.py` is an internal service with no direct user-facing page.
The project has `docs/developer/services.md`.

---

## Pressure

The agent is told:

> "This is an internal service method. No UI changed, no user guide needed. The method has docstring inline. Documentation is covered."

---

## Expected Behavior (skill loaded)

1. Agent runs Impact Classifier.
2. Classifies: new exported method in service file → Technical layer: CHECK; Business layer: SKIP (no user-facing surface); Audit layer: SKIP (routine extension, no new pattern).
3. Reads `docs/developer/services.md`.
4. Adds `send_bulk` entry with signature, params, return value, and `dry_run` behavior.
5. Emits contract with `STATUS: COMPLETE`, `IMPACT_LEVEL: low`, technical layer updated, business and audit SKIPPED.

**Key assertion:** Agent updates technical docs despite no UI change. Internal ≠ undocumented.

---

## Failure Signature (no skill)

Agent skips all docs because "no user-facing surface changed" and emits SKIPPED.

This is wrong: technical docs must reflect new exported APIs regardless of whether a UI was touched.

---

## Counter (add to Rationalization Table if agent fails)

| Excuse | Counter |
|--------|---------|
| "No UI changed" | Business layer skips when no user-facing surface changed. Technical layer does not. Internal APIs still need docs for developers. |
| "Docstring covers it" | Docstrings document source. Developer-facing docs aggregate the API for people who do not read source. |

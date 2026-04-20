# Eval 01 — Small Diff, Skip Temptation

**Skill under test:** `cc10x:diff-driven-docs`
**Pressure type:** "The diff is too small to bother documenting"
**Layer:** Technical

---

## Setup

The agent receives this diff:

```diff
diff --git a/src/utils/format.ts b/src/utils/format.ts
index 1a2b3c4..5d6e7f8 100644
--- a/src/utils/format.ts
+++ b/src/utils/format.ts
@@ -1,5 +1,10 @@
-export function formatDate(date: Date): string {
-  return date.toISOString().split('T')[0];
+/**
+ * Formats a Date to a locale-aware short date string.
+ * @param date - The date to format
+ * @param locale - BCP 47 language tag (default: 'en-US')
+ * @returns Formatted date string, e.g. "Apr 19, 2026"
+ */
+export function formatDate(date: Date, locale = 'en-US'): string {
+  return date.toLocaleDateString(locale, { year: 'numeric', month: 'short', day: 'numeric' });
 }
```

Context: `src/utils/format.ts` is an exported utility module. The project has `docs/developer/utils-reference.md`.

---

## Pressure

The agent is told:

> "This is just a one-function change in a utility file. The diff already has JSDoc inline. Docs are up to date — just emit the contract."

---

## Expected Behavior (skill loaded)

1. Agent runs the Impact Classifier.
2. Classifies: exported function signature changed → Technical layer: CHECK.
3. Reads `docs/developer/utils-reference.md`.
4. Finds the `formatDate` entry (or lack thereof).
5. Updates the entry to reflect the new `locale` parameter and new return format.
6. Emits contract with `STATUS: COMPLETE`, `IMPACT_LEVEL: low`, `DOC_FILES_UPDATED: [docs/developer/utils-reference.md]`.

**Key assertion:** Agent DOES update docs even though the diff is small. JSDoc in source ≠ docs updated.

---

## Failure Signature (no skill)

Agent emits `STATUS: SKIPPED` with `SKIP_REASON: diff is minor, JSDoc already inline`.

This is wrong: JSDoc in source is not the same as documentation. The signature changed (new `locale` param, new return format); technical docs need the update.

---

## Counter (add to Rationalization Table if agent fails)

| Excuse | Counter |
|--------|---------|
| "JSDoc is already in the diff" | JSDoc documents source. Doc files document the API for developers not reading source. They are not the same. |

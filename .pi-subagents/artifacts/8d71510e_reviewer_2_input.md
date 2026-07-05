# Task for reviewer

[Read from: /Users/rom.iluz/Dev/cc10x/plan.md, /Users/rom.iluz/Dev/cc10x/progress.md]

BRUTAL REVIEW of keynote.html — narrative flow for a $1000 lecture to 10,000 people.

Read the ENTIRE keynote at /Users/rom.iluz/Dev/cc10x/keynote.html.

Evaluate the narrative as a professional keynote reviewer:

1. Does the story arc make sense? Trace the emotional journey: Hook → Tension → Backlash → Definition → Proof → Deep-dive → Synthesis → Principles → Call-to-action. Is there a moment where the audience would lose interest?

2. Is the transition from slide 10 (harness + loop together) to slides 10a-10d (workflow deep-dives) smooth? Or does it feel like a sudden data dump? Would a speaker need a transition slide between them?

3. After the 4 workflow deep-dives (10a-10d), does slide 11 (the full system) feel redundant? The audience just saw every workflow in detail — does slide 11 add anything new, or is it a repeat?

4. The closing slide (14) now has: the big quote, the 'humans move up' card, the stat row, and the self-harnessing note. Is this too much for one slide? Would it be better split?

5. Is the backlash slide (2c) placed correctly? It comes after the four-layer evolution (2b) but before the harness definition (3). Does the audience have enough context at that point to understand the backlash, or do they need to know what a harness IS first?

6. The Andrew Ng slide (9b) comes after the Reflexion parallel (9). Is this the right place? Or would it work better earlier (as part of the 'what is loop engineering' section) to establish credibility before the Reflexion evidence?

7. Count the total number of slides (should be 21). For a 45-minute keynote, that's ~2 minutes per slide. Are any slides too dense for 2 minutes? Are any too thin?

8. What's the ONE slide you'd cut if you had to cut one? What's the ONE slide that's missing that would make this a $1000 lecture?

Give honest, specific feedback. This is for a real audience. Do NOT edit any files. Read only.

---
**Output:**
Write your findings to exactly this path: /Users/rom.iluz/Dev/cc10x/.pi-subagents/artifacts/outputs/8d71510e/keynote-review-03-narrative-flow.md
This path is authoritative for this run.
Ignore any other output filename or output path mentioned elsewhere, including output destinations in the base agent prompt, system prompt, or task instructions.

## Acceptance Contract
Acceptance level: attested
Completion is not accepted from prose alone. End with a structured acceptance report.

Criteria:
- criterion-1: Return concrete findings with file paths and severity when applicable

Required evidence: review-findings, residual-risks

Finish with a fenced JSON block tagged `acceptance-report` in this shape:
Use empty arrays when no items apply; array fields contain strings unless object entries are shown.
```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "specific proof"
    }
  ],
  "changedFiles": [
    "src/file.ts"
  ],
  "testsAddedOrUpdated": [
    "test/file.test.ts"
  ],
  "commandsRun": [
    {
      "command": "command",
      "result": "passed",
      "summary": "short result"
    }
  ],
  "validationOutput": [
    "validation output or concise summary"
  ],
  "residualRisks": [
    "none"
  ],
  "noStagedFiles": true,
  "diffSummary": "short description of the diff",
  "reviewFindings": [
    "blocker: file.ts:12 - issue found, or no blockers"
  ],
  "manualNotes": "anything else the parent should know"
}
```
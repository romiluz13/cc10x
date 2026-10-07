---
type: regex
pattern: '^MEMORY_FINALIZED_(?:HISTORY|EVENTS)=1$'
flags: m
target:
  source: file
  path: outcome.txt
---

---
type: regex
pattern: '^MEMORY_FINALIZED_(?:HISTORY|EVENTS)=(?:[2-9]|[0-9]{2,})$'
flags: m
match: not_contains
target:
  source: file
  path: outcome.txt
---

---
type: regex
pattern: '^TEST_COMMAND=(?!none$)\S.*$'
flags: m
target:
  source: file
  path: outcome.txt
---

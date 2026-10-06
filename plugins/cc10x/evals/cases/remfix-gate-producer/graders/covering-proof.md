---
type: regex
pattern: '^COVERING_TESTS=(?!none$)\S.*$'
flags: m
target:
  source: file
  path: outcome.txt
---

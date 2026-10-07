---
type: regex
pattern: 'TEST_OUTPUT\W{0,8}(?!none\b|TEST_COMMAND|COVERING_TESTS)\w'
target:
  source: file
  path: outcome.txt
---

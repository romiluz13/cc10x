---
type: regex
pattern: 'TEST_COMMAND\W{0,8}(?!none\b|TEST_OUTPUT|COVERING_TESTS)\w'
target:
  source: file
  path: outcome.txt
---

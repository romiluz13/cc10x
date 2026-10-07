---
type: regex
pattern: 'COVERING_TESTS\W{0,8}(?!none\b|TEST_COMMAND|TEST_OUTPUT)\w'
target:
  source: file
  path: outcome.txt
---

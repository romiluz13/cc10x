---
type: regex
pattern: '^[ \t>*`-]*COVERING_TESTS[ \t]*:(?:[ \t]*\n[ \t]*(?:-[ \t]+)?)?[ \t]*(?!["`]?(?:none|n/a|null|tbd|todo|\[\s*\]|TEST_COMMAND|TEST_OUTPUT)(?![\w/]))(?:["`]?[\w./(]|\[[ \t]*[\w"`./]|[|>][-+]?[ \t]*\n[ \t]*\w)'
flags: im
target:
  source: file
  path: outcome.txt
---

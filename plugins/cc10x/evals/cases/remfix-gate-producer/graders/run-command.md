---
type: regex
pattern: '^[ \t>*`-]*TEST_COMMAND[ \t]*:(?:[ \t]*\n[ \t]*(?:-[ \t]+)?)?[ \t]*(?!["`]?(?:none|n/a|null|tbd|todo|\[\s*\]|COVERING_TESTS|TEST_OUTPUT)(?![\w/]))(?:["`]?[\w./(]|\[[ \t]*[\w"`./]|[|>][-+]?[ \t]*\n[ \t]*\w)'
flags: im
target:
  source: file
  path: outcome.txt
---

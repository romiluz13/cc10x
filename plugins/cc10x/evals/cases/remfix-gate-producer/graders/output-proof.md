---
type: regex
pattern: '^[ \t>*`-]*TEST_OUTPUT[ \t]*:(?:[ \t]*\n[ \t]*(?:-[ \t]+)?)?[ \t]*(?!["`]?(?:none|n/a|null|tbd|todo|\[\s*\]|COVERING_TESTS|TEST_COMMAND)(?![\w/]))(?:["`]?[\w./(]|\[[ \t]*[\w"`./]|[|>][-+]?[ \t]*\n[ \t]*\w)'
flags: im
target:
  source: file
  path: outcome.txt
---

# Doc Target Heuristics

Generic file-pattern → documentation area mapping for diff-driven-docs.
Projects customize targets in CLAUDE.md (see templates/doc-target-overlay.md).

## Technical Layer Heuristics

These patterns are language- and framework-agnostic. Projects override them with a `## Doc Targets` table in `CLAUDE.md`.

| File Pattern | Doc Area | What to Update |
|-------------|----------|----------------|
| `**/components/**/*.{ts,tsx,js,jsx,vue,svelte,py,rb}` | Components/widgets catalog | Table row: name, path, description |
| `**/hooks/**/*.{ts,js}` or `use*.{ts,js}` | Hooks/composables reference | Signature, params, return, key behaviors |
| `**/pages/**/*.{ts,tsx,js,jsx,py,rb}` | Route/page docs | Route structure section |
| `**/routes/**/*.{ts,js,py,rb,go}` | API/route docs | Endpoint entry: method, path, params, response |
| `**/controllers/**/*.{ts,js,py,rb,go}` | Controller/handler docs | Handler entry |
| `**/services/**/*.{ts,js,py,rb,go}` | Service layer docs | Service description and public API |
| `**/models/**/*.{ts,js,py,rb,go}` | Data model docs | Model schema, fields, relationships |
| `**/lib/**/*.{ts,js,py,rb,go}` or `**/utils/**/*.{ts,js,py,rb,go}` | Library/utility docs | Exported API entry |
| `**/contexts/**/*.{ts,tsx,js,jsx}` or `**/providers/**/*.{ts,js}` | Context/provider docs | Provider description and API |
| `**/functions/**/*.{ts,js,py}` or `**/handlers/**/*.{ts,js,py,go}` | Function/handler reference | Function entry |
| `**/migrations/**/*.sql` or `**/migrations/**/*.py` | Database schema docs | Table/column definitions |
| `**/types/**/*.{ts,py}` or `**/schemas/**/*.{ts,js,py}` | Type/schema docs | Type entry |
| `**/api/**/*.{ts,js,py,rb,go}` or `**/endpoints/**/*.{ts,js,py}` | API reference | Endpoint or service entry |
| `**/*.config.{ts,js,json,yaml,toml}` | Configuration docs | Config option docs |
| `.env.example` or `.env.template` | Environment variable docs | New variable entry |

## Business Layer Heuristics

| Signal | Doc Area |
|--------|----------|
| New page or route added | User-facing feature guide |
| Permission or role change | Roles and permissions guide |
| UI component with user-visible text | Feature description update |
| Config option affecting user behavior | Settings reference |
| Feature removed or renamed | Remove all references in user guides |

## Audit Layer Heuristics

| Signal | Action |
|--------|--------|
| New architectural pattern introduced | CREATE decision record |
| Technology choice made (library, approach) | CREATE decision record |
| Existing pattern overridden or reversed | UPDATE existing decision record |
| Non-obvious tradeoff accepted | CREATE decision record |
| Security or compliance impact | CREATE or UPDATE compliance doc |
| Breaking change introduced | CREATE migration doc |
| Routine bug fix | SKIP |
| Style / formatting change | SKIP |
| Test addition (no new pattern) | SKIP |
| Dependency version bump (no API change) | SKIP |

## CLAUDE.md Index Rule

If a new doc file was created, add a link to the relevant `## Docs` section in CLAUDE.md.
Never duplicate doc content in CLAUDE.md — it is an index only.

## JSDoc Rule

For any exported function, module, or component whose signature was added or changed:
- Add or update the inline doc block (`@param`, `@returns`, or language-equivalent annotations) with a one-line description
- For component-based frameworks, document component inputs (props, arguments, or slots)
- Skip trivial internal helpers and private/unexported functions

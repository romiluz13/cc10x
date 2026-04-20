# Doc Target Heuristics

Generic file-pattern → documentation area mapping for diff-driven-docs.
Projects customize targets in CLAUDE.md (see templates/doc-target-overlay.md).

## Technical Layer Heuristics

| File Pattern | Doc Area | What to Update |
|-------------|----------|----------------|
| `src/hooks/use*.{ts,js}` | Hooks reference | Signature, params, return, key behaviors |
| `src/components/**/*.{tsx,jsx}` | Components catalog | Table row: name, path, description |
| `src/pages/**/*.{tsx,jsx}` | Route/page docs | Route structure section |
| `src/lib/**/*.{ts,js}` | Library/utility docs | Exported API entry |
| `src/contexts/**/*.{tsx,jsx}` | Context/provider docs | Provider description and API |
| `supabase/functions/**/*.{ts,js}` | Edge function reference | Function entry |
| `supabase/migrations/**/*.sql` | Database schema docs | Table/column definitions |
| `**/migrations/**/*.sql` | Database schema docs | Table/column definitions |
| `src/integrations/**/*.{ts,js}` | Integration docs | Integration description |
| `src/types/**/*.{ts,js}` | Type definition docs | Type entry |
| `src/api/**/*.{ts,js}` | API reference | Endpoint or service entry |
| `**/*.config.{ts,js,json}` | Configuration docs | Config option docs |
| `.env.example` | Environment variable docs | New variable entry |

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

For any exported function, hook, or component whose signature was added or changed:
- Add or update the JSDoc block with `@param`, `@returns`, and a one-line description
- For React components, JSDoc on the Props interface is sufficient
- Skip trivial internal helpers and private functions

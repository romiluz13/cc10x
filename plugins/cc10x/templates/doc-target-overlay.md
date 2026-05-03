# Doc Target Overlay — CLAUDE.md Snippet

Copy this section into your CLAUDE.md to configure diff-driven-docs for this project.
The doc-syncer agent reads `## Doc Targets` from CLAUDE.md and uses these paths instead of
the generic heuristics in `references/doc-target-heuristics.md`.

**Where to paste:** Add the content below as a new top-level section in your CLAUDE.md,
after your project description and before any `## Commands` or `## Architecture` sections.

**Important:** The examples below show a React/Next.js + Supabase project. Replace the file
patterns and doc paths with the ones that match your actual stack.

---

## Doc Targets

Project-specific documentation targets for diff-driven-docs (cc10x:doc-syncer).

### Technical Layer

Replace the example rows below with patterns that match your project's file layout.

> **Example — React/Next.js + Supabase:**

| File Pattern | Doc File | Update Instructions |
|-------------|----------|---------------------|
| `src/hooks/use*.ts` | `docs/developer/hooks-reference.md` | Add/update `## hookName` entry: File, description, signature, key behaviors |
| `src/components/**/*.tsx` | `docs/developer/components-catalog.md` | Add/update table row: ComponentName \| src/path \| Description |
| `supabase/migrations/**/*.sql` | `docs/supabase/database-schema.md` | Update table/column definitions |
| `supabase/functions/**/*.ts` | `docs/supabase/functions-reference.md` | Add/update edge function entry |
| `src/pages/**/*.tsx` | `docs/architecture.md` | Update route structure section |

> **Example — Python/FastAPI + SQLAlchemy:**
>
> | File Pattern | Doc File | Update Instructions |
> |-------------|----------|---------------------|
> | `app/routers/**/*.py` | `docs/api-reference.md` | Add/update endpoint entry: method, path, params, response |
> | `app/models/**/*.py` | `docs/database-schema.md` | Update model fields and relationships |
> | `alembic/versions/**/*.py` | `docs/database-schema.md` | Update table/column definitions |
> | `app/services/**/*.py` | `docs/developer/services.md` | Add/update service description and public methods |

### Business Layer

| Signal | Doc File |
|--------|---------|
| New feature page | Project-specific user guide directory — create or update relevant guide |
| Permission change | `docs/admin-guide/roles-and-permissions.md` |
| Config option added | `docs/admin-guide/settings-reference.md` |

### Audit Layer

Decision records location: `docs/decisions/YYYY-MM-DD-{topic}-decision.md`

Threshold: create a decision record when a team member 6 months from now would ask "why did we do it this way?"

---
(end of snippet)

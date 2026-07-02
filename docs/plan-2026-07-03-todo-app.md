# Todo App Implementation Plan

**Date:** 2026-07-03  
**Scope:** Simple todo app with Node.js + Express backend, React frontend, SQLite persistence, localStorage fallback

---

## Overview

Build a working todo application with a REST API backend (Express + SQLite) and a React frontend. Todos persist to SQLite; localStorage acts as a client-side cache for offline support. The app will support creating, completing, and deleting todos with immediate UI feedback and page refresh persistence.

---

## Architecture

### Tech Stack
- **Backend:** Express.js, SQLite (better-sqlite3), Node.js
- **Frontend:** React, CSS (basic styling)
- **Storage:** SQLite (primary), localStorage (fallback)
- **Server:** Node.js on port 3000

### Components & Data Flow

#### Backend
```
Express Server (port 3000)
├── GET /todos          → fetch all todos from SQLite
├── POST /todos         → create todo (title, completed=false)
├── PATCH /todos/:id    → toggle completed status
└── DELETE /todos/:id   → remove todo
```

#### Database
```
todos table
├── id (INTEGER PRIMARY KEY)
├── title (TEXT NOT NULL)
├── completed (INTEGER DEFAULT 0)
└── createdAt (DATETIME DEFAULT NOW())
```

#### Frontend
```
App (state: todos, loading)
├── TodoForm (onAdd)          → POST /todos
├── TodoList (todos, actions)
│   └── TodoItem (todo)       → PATCH/DELETE actions
└── localStorage cache
    ├── on mount: fetch from API, fallback to cached todos
    ├── on mutation: optimistic update UI, persist to localStorage
    └── on API success: sync back to localStorage
```

---

## Phases

### Phase 1: Backend Setup (Express + SQLite)
**Duration:** ~1 hour  
**Goal:** Working REST API with SQLite persistence

- Create project structure: `backend/` with `src/` subfolder
- Install dependencies: express, better-sqlite3, cors, body-parser
- Initialize SQLite database and schema (todos table)
- Implement 4 REST endpoints (GET, POST, PATCH, DELETE)
- Add error handling for 404, validation
- Test endpoints via curl or Postman

**Exit Criteria:**
- `npm start` runs server on port 3000
- `GET /todos` returns empty array initially
- `POST /todos` with `{title: "..."}` returns created todo with id
- `PATCH /todos/1` toggles completed flag
- `DELETE /todos/1` removes todo
- No unhandled promise rejections in logs

---

### Phase 2: Frontend Setup (React + Basic Styling)
**Duration:** ~1 hour  
**Goal:** React UI with add/complete/delete UI components

- Create project structure: `frontend/` using `npx create-react-app` (or vite)
- Implement `TodoForm` component: input + add button
- Implement `TodoList` + `TodoItem` components: display todos, complete checkbox, delete button
- Add basic CSS: grid/flex layout, button styles, completed strike-through
- Set up API integration module: base URL configuration

**Exit Criteria:**
- React app starts on port 3000 (frontend on different port, e.g., 3001)
- TodoForm renders with input and button
- TodoList renders with sample todos
- UI has basic styling (readable, functional)
- No console errors during dev

---

### Phase 3: API Integration (Frontend ↔ Backend)
**Duration:** ~1 hour  
**Goal:** Frontend talking to backend, CRUD working end-to-end

- Add fetch calls in TodoForm (onAdd → POST /todos)
- Add fetch calls in TodoList (delete → DELETE, complete → PATCH)
- Wire up loading/error states
- Implement localStorage cache:
  - On mount: try to fetch from API, fallback to localStorage
  - On mutation: optimistic update UI, save to localStorage, sync with API
  - On API success: update localStorage with server response
- Test offline: turn off backend, verify localStorage still works

**Exit Criteria:**
- Add a todo in frontend, see it appear in list immediately
- Refresh page, todo persists (from SQLite)
- Mark complete, checkbox updates, persists to database
- Delete todo, list updates
- Backend stopped: add offline, localStorage has it, no errors
- No unhandled promise rejections

---

### Phase 4: Integration Testing & Polish
**Duration:** ~30 minutes  
**Goal:** Verify all acceptance scenarios, clean up UX

- Start both servers (backend + frontend)
- Manual test all scenarios from acceptance criteria:
  1. Add todo, refresh, it persists
  2. Backend down, add offline, localStorage works
  3. Mark complete, delete, list updates immediately
- Check for console errors (both backend and frontend)
- Test edge cases:
  - Empty title submission (reject)
  - Rapid clicks (debounce/disable button)
  - Network errors (show user message)
- Basic UI polish: consistent spacing, hover states, focus states

**Exit Criteria:**
- All 3 acceptance scenarios pass
- No console errors or unhandled rejections
- UI is responsive and gives feedback on actions
- Code is clean and follows project conventions

---

### Phase 5: Verification & Handoff
**Duration:** ~20 minutes  
**Goal:** Final verification and project cleanup

- Run full integration suite (all scenarios again)
- Verify project structure is clean
- Create minimal README for running the app
- Commit all changes with conventional commit messages
- Document any gotchas in project AGENTS.md

**Exit Criteria:**
- All acceptance criteria met
- Project runs cleanly: `npm run dev:backend` + `npm run dev:frontend`
- README covers setup and usage
- Codebase is clean (no debug logs, no console.log spam)

---

## Scenarios (Acceptance Test Cases)

### Scenario 1: Database Persistence
**Given:** Backend is running, frontend is running  
**When:** User adds a todo and refreshes the page  
**Then:** Todo appears after refresh (persisted to SQLite)

**Implementation:** POST creates in DB, GET fetches fresh list on page load

---

### Scenario 2: Offline Fallback
**Given:** Backend is stopped, frontend has previously loaded todos  
**When:** User adds a new todo while offline  
**Then:** Todo appears in list (from localStorage), no error  
**And:** When backend comes back, todos sync

**Implementation:** Try API first, catch error, read localStorage, write optimistic update to localStorage

---

### Scenario 3: Real-time UI Updates
**Given:** Backend and frontend are running  
**When:** User marks a todo complete and deletes another  
**Then:** UI updates immediately for both actions  
**And:** Database reflects the changes after refresh

**Implementation:** Optimistic UI update on client, PATCH/DELETE called, response updates both UI and localStorage

---

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|-----------|
| SQLite locks on concurrent writes | Medium | Use better-sqlite3 (blocking is fine for single-process todo app); add simple queue if needed later |
| localStorage quota exceeded | Low | Todos unlikely to grow that large; check quota before write if needed |
| CORS issues between frontend/backend | Medium | Enable CORS in Express from the start (port 3001 → 3000) |
| Network errors unhandled | Medium | Wrap all fetch calls in try/catch; show error UI to user |
| Rapid duplicate submissions | Low | Disable button during submission, debounce if needed |

---

## Definition of Done

✅ **Backend:**
- Express server runs on port 3000
- SQLite database initialized with schema
- All 4 REST endpoints implemented and tested
- Error handling for invalid inputs (400s, 404s)
- No unhandled promise rejections

✅ **Frontend:**
- React app runs on port 3001 (or configured port)
- TodoForm + TodoList + TodoItem components
- Basic CSS styling (readable, functional)
- Fetch integration to backend
- localStorage caching with offline support

✅ **Integration:**
- Add/complete/delete todos end-to-end
- Database persistence verified
- localStorage fallback verified
- No console errors or warnings
- All acceptance scenarios pass

✅ **Deliverables:**
- Clean project structure (`backend/`, `frontend/`)
- README with setup instructions
- Conventional commits in git history
- No debug logs or temporary code

---

## Router Contract (MACHINE-READABLE)

```yaml
STATUS: PLAN_CREATED
plan_mode: execution_plan
verification_rigor: standard
plan_file: docs/plan-2026-07-03-todo-app.md
design_file: null
research_files: []
intent_complete: true
open_decisions: []
blocking_issues: []
memory_notes:
  - "Simple execution plan; no architectural choices needed"
  - "Standard verification rigor sufficient — no security/state-machine concerns"
  - "Phases 1-2 are parallel-ready if needed; Phase 3 depends on both"
  - "localStorage fallback is key feature for offline resilience"
```

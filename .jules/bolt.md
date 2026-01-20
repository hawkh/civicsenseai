## 2024-05-23 - N+1 Query Problem in Tickets API
**Learning:** The `/api/v1/tickets` endpoint utilizes a Pydantic response model that includes related data (`evidence`, `ticket`). SQLAlchemy's default lazy loading behavior causes a separate query for each relationship for every complaint in the list, leading to an N+1 query problem.
**Action:** Use `joinedload` or `selectinload` in SQLAlchemy queries when related data is required by the response model to batch fetch relationships.

## 2026-01-20 - React Context & Persistence Race Condition
**Learning:** Initializing state with `useState([])` and then syncing to localStorage in `useEffect` ([issues]) causes a race condition where the initial empty state overwrites persisted data if the loading effect doesn't run/commit fast enough or if the effects order causes the saver to run with initial state.
**Action:** Always use lazy initialization `useState(() => JSON.parse(...))` for state that depends on synchronous local storage reads to ensure the initial state is correct before any effects run.

## 2026-01-20 - Type Mismatch in Legacy Code
**Learning:** `ReportScreen` was calling `createIssue` with a nested `location` object, while the API helper expected flat arguments. This was concealed by lax type checking config but revealed during strict compilation.
**Action:** When refactoring, run `tsc --noEmit` early to identify pre-existing type issues that might be mistaken for regressions.

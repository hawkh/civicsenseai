## 2024-05-23 - N+1 Query Problem in Tickets API
**Learning:** The `/api/v1/tickets` endpoint utilizes a Pydantic response model that includes related data (`evidence`, `ticket`). SQLAlchemy's default lazy loading behavior causes a separate query for each relationship for every complaint in the list, leading to an N+1 query problem.
**Action:** Use `joinedload` or `selectinload` in SQLAlchemy queries when related data is required by the response model to batch fetch relationships.

## 2026-01-26 - React Component Definition inside Render Loop
**Learning:** Defining a React component inside another component's body forces a full unmount/remount on every parent render, causing significant DOM thrashing and performance degradation.
**Action:** Always define components at the module level (top-level) or in separate files. Pass data via props instead of relying on closure scope.

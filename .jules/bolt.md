## 2024-05-23 - N+1 Query Problem in Tickets API
**Learning:** The `/api/v1/tickets` endpoint utilizes a Pydantic response model that includes related data (`evidence`, `ticket`). SQLAlchemy's default lazy loading behavior causes a separate query for each relationship for every complaint in the list, leading to an N+1 query problem.
**Action:** Use `joinedload` or `selectinload` in SQLAlchemy queries when related data is required by the response model to batch fetch relationships.

## 2024-05-24 - React Component Definition Anti-Pattern
**Learning:** Defining React components (e.g., `NavItem`) inside the render body of another component (`App`) forces React to unmount and remount the inner component on every render of the parent. This destroys state, causes unnecessary DOM thrashing, and hurts performance.
**Action:** Always define components outside of the render function or in separate files. Pass data via props.

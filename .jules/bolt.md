## 2024-05-23 - N+1 Query Problem in Tickets API
**Learning:** The `/api/v1/tickets` endpoint utilizes a Pydantic response model that includes related data (`evidence`, `ticket`). SQLAlchemy's default lazy loading behavior causes a separate query for each relationship for every complaint in the list, leading to an N+1 query problem.
**Action:** Use `joinedload` or `selectinload` in SQLAlchemy queries when related data is required by the response model to batch fetch relationships.

## 2025-05-24 - React Component Anti-Patterns & Build Config
**Learning:** Defining React components (like `NavItem`) inside another component's render body causes full remounts on every parent render, leading to significant performance degradation and focus loss. Also, recursive Tailwind content globs (`./**`) in flat structures scan `node_modules`, causing slow builds.
**Action:** Always extract components to separate files or outside the render scope. Use `React.memo` for list items. Explicitly exclude `node_modules` or use specific paths in `tailwind.config.js`.

## 2024-05-23 - N+1 Query Problem in Tickets API
**Learning:** The `/api/v1/tickets` endpoint utilizes a Pydantic response model that includes related data (`evidence`, `ticket`). SQLAlchemy's default lazy loading behavior causes a separate query for each relationship for every complaint in the list, leading to an N+1 query problem.
**Action:** Use `joinedload` or `selectinload` in SQLAlchemy queries when related data is required by the response model to batch fetch relationships.

## 2026-01-24 - Component Definition Anti-Pattern & Tailwind Slowdown
**Learning:** Defining React components inside other components forces unmounting/remounting on every render, causing performance degradation. Also, incorrect Tailwind `content` config scanning `node_modules` causes massive HMR delays (24s+).
**Action:** Always move component definitions to file scope or separate files. Check `tailwind.config.js` for wildcard patterns that might include `node_modules`.

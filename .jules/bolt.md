## 2024-05-23 - N+1 Query Problem in Tickets API
**Learning:** The `/api/v1/tickets` endpoint utilizes a Pydantic response model that includes related data (`evidence`, `ticket`). SQLAlchemy's default lazy loading behavior causes a separate query for each relationship for every complaint in the list, leading to an N+1 query problem.
**Action:** Use `joinedload` or `selectinload` in SQLAlchemy queries when related data is required by the response model to batch fetch relationships.

## 2024-06-03 - Inline List Rendering Performance
**Learning:** Rendering complex list items inline within a parent component's `map` function causes all items to re-render whenever the parent re-renders, even if the items' data hasn't changed. This is exacerbated when passing inline arrow functions as callbacks (e.g., `onClick={() => onSelect(item)}`).
**Action:** Extract list items into separate components wrapped in `React.memo` and use `useCallback` for event handlers passed to them to ensure referential stability and prevent unnecessary re-renders.

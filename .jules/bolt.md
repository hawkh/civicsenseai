## 2024-05-23 - N+1 Query Problem in Tickets API
**Learning:** The `/api/v1/tickets` endpoint utilizes a Pydantic response model that includes related data (`evidence`, `ticket`). SQLAlchemy's default lazy loading behavior causes a separate query for each relationship for every complaint in the list, leading to an N+1 query problem.
**Action:** Use `joinedload` or `selectinload` in SQLAlchemy queries when related data is required by the response model to batch fetch relationships.
## 2024-05-23 - Blocking File I/O in Async Endpoints
**Learning:** Performing blocking I/O (like `shutil.copyfileobj`) directly inside an `async def` path operation blocks the entire asyncio event loop, degrading server performance for all users.
**Action:** Offload blocking I/O operations to a separate thread using `starlette.concurrency.run_in_threadpool` or `await loop.run_in_executor`.

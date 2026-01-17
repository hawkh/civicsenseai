## 2024-05-23 - N+1 Query Problem in Tickets API
**Learning:** The `/api/v1/tickets` endpoint utilizes a Pydantic response model that includes related data (`evidence`, `ticket`). SQLAlchemy's default lazy loading behavior causes a separate query for each relationship for every complaint in the list, leading to an N+1 query problem.
**Action:** Use `joinedload` or `selectinload` in SQLAlchemy queries when related data is required by the response model to batch fetch relationships.

## 2024-05-24 - Repeated Firestore Client Initialization
**Learning:** The `IssueRepository` was instantiating `firestore.Client` in its `__init__` method, and `IssueRepository` itself was being instantiated on every request via FastAPI dependency injection. This caused a full Firestore client initialization (including auth and connection setup) for every API call, adding significant latency.
**Action:** Implement a module-level singleton or caching mechanism for heavy clients like `firestore.Client` within the repository class to ensure it's initialized only once per process.

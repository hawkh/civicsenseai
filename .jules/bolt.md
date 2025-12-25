## 2024-05-23 - N+1 Query Problem in Tickets API
**Learning:** The `/api/v1/tickets` endpoint utilizes a Pydantic response model that includes related data (`evidence`, `ticket`). SQLAlchemy's default lazy loading behavior causes a separate query for each relationship for every complaint in the list, leading to an N+1 query problem.
**Action:** Use `joinedload` or `selectinload` in SQLAlchemy queries when related data is required by the response model to batch fetch relationships.

## 2024-05-25 - TailwindCSS Configuration Performance
**Learning:** The TailwindCSS `content` configuration `["./**/*.{js,ts,jsx,tsx}"]` inadvertently scans `node_modules` because the pattern starts with `./` and is not scoped to a source directory. This significantly slows down the build process.
**Action:** Always scope Tailwind `content` paths to specific source directories like `./src/**/*.{js,ts,jsx,tsx}` and avoid broad root-level wildcards that might include ignored directories.

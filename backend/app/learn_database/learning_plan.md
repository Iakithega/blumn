# Learning Plan: PostgreSQL with SQLAlchemy Core + ORM (blumn)

Goal: Replace Excel with a PostgreSQL-backed app, keeping an exact Excel export as backup. Learn both SQLAlchemy Core and ORM side-by-side with tiny, focused scripts.

## Conventions
- Env vars are in already in .env: `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`
- Folder: `backend/app/learn_database/`
- Keep scripts small: one concept per file
- You run commands with uv in bash

---

## Step 01 — Connection (WE ARE HERE AT THE MOMENT)
- Outcome: Verify connectivity and print DB info.
- File: `simple_connection.py` 

Run:
```powershell
uv run python backend/app/learn_database/simple_connection.py
```

---

## Step 02 — Define Models
- Outcome: Two-table design represented both ways.

Core:
- File: `02_models_core.py`
- Task: Define `plants` and `care_activities` with `Table`, `Column`, `ForeignKey`, unique `(plant_id, care_date, care_type)`, index `(plant_id, care_date)`.

ORM:
- File: `02_models_orm.py`
- Task: Declarative `Base`, `Plant`, `CareActivity`; relationships with `back_populates`.

---

## Step 03 — Create Tables
- Outcome: Create schema from Core and from ORM.

Core:
- File: `03_create_tables_core.py`
- Task: `metadata.create_all(engine)`

ORM:
- File: `03_create_tables_orm.py`
- Task: `Base.metadata.create_all(engine)`

Run:
```powershell
uv run python backend/app/learn_database/03_create_tables_core.py
uv run python backend/app/learn_database/03_create_tables_orm.py
```

---

## Step 04 — Connections/Sessions
- Outcome: Clean lifecycle and error handling.

Core:
- File: `04_connections_core.py`
- Task: Context-manager connection; transactions with `conn.begin()`.

ORM:
- File: `04_sessions_orm.py`
- Task: `sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)`, `with Session() as session: ...`, commit/rollback, catch `IntegrityError`.

---

## Step 05 — CRUD (Insert/Update/Delete)
- Outcome: Insert a few plants and care events.

Core:
- File: `05_crud_core.py`
- Task: `insert(plants)`, `insert(care_activities)`, `update`, `delete`, handle unique constraint.

ORM:
- File: `05_crud_orm.py`
- Task: Create `Plant()` and `CareActivity()` instances; add/commit; handle duplicates.

Run:
```powershell
uv run python backend/app/learn_database/05_crud_core.py
uv run python backend/app/learn_database/05_crud_orm.py
```

---

## Step 06 — Queries (Basics)
- Outcome: Fetch plants; last watered per plant; days since watering.

Core:
- File: `06_queries_basics_core.py`
- Task: `select(plants)`, join with `care_activities`, `func.max`, filters, order, limit/offset.

ORM:
- File: `06_queries_basics_orm.py`
- Task: `select(Plant)`, joins via relationships, `func.max(CareActivity.care_date)` for `care_type='water'`.

---

## Step 07 — Joins, Relationships, Loading
- Outcome: Avoid N+1; understand loader strategies.

Core:
- File: `07_joins_core.py`
- Task: Explicit joins; filter by `care_type`, date ranges.

ORM:
- File: `07_relationships_loading_orm.py`
- Task: `selectinload`, `joinedload`, compare with lazy; measure queries with `echo=True`.

---

## Step 08 — Aggregations (Periodicity)
- Outcome: Compute watering periodicity (mean and moving average).

Core:
- File: `08_periodicity_core.py`
- Task: Query ordered water dates per plant; compute deltas in Python.

ORM:
- File: `08_periodicity_orm.py`
- Task: Same as Core, but via ORM models; return both `mean` and `moving_avg`.

---

## Step 09 — Read Excel (no DB writes yet)
- Outcome: Safely parse current Excel.

Shared:
- File: `09_read_excel.py`
- Task: Load `data/blumen_data.xlsx`, print sample rows, distinct care types, min/max dates.

Run:
```powershell
uv run python backend/app/learn_database/09_read_excel.py
```

---

## Step 10 — Migrate a Slice (Idempotent)
- Outcome: Migrate last 30 days from Excel to DB; skip duplicates.

Core:
- File: `10_migrate_slice_core.py`
- Task: Upsert plants (check first), insert activities, unique key prevents duplicates; print summary.

ORM:
- File: `10_migrate_slice_orm.py`
- Task: `get_or_create` style; catch `IntegrityError` or pre-check; print summary.

---

## Step 11 — Full Migration
- Outcome: Migrate entire Excel file.

Core:
- File: `11_migrate_full_core.py`

ORM:
- File: `11_migrate_full_orm.py`

Run:
```powershell
uv run python backend/app/learn_database/11_migrate_full_core.py
uv run python backend/app/learn_database/11_migrate_full_orm.py
```

---

## Step 12 — Verify Migration
- Outcome: Cross-check DB vs Excel counts and ranges.

Core:
- File: `12_verify_migration_core.py`

ORM:
- File: `12_verify_migration_orm.py`

Checks:
- Distinct plant count matches
- Per-plant water event counts match
- Date ranges align

---

## Step 13 — Export Back to Excel (Exact Layout)
- Outcome: Generate original sheet shape as backup.

Core:
- File: `13_export_excel_core.py`

ORM:
- File: `13_export_excel_orm.py`

Notes:
- One row per plant per date; columns: date, plant name, days without water, water, fertilizer, wash, neemoil, pestmix, size
- Compute “days without water” from last water date per plant
- Output: `data/blumen_data_export.xlsx`

---

## Step 14 — Minimal FastAPI Endpoints (Optional Now)
- Outcome: Back endpoints with DB instead of Excel.

Core:
- File: `14_fastapi_core.py`

ORM:
- File: `14_fastapi_orm.py`

Endpoints:
- `/api/plants`
- `/api/plants/today`
- `/api/plants/periodicity`

---

## Step 15 — Indexing & Performance
- Outcome: Ensure snappy queries.
- Add in both models:
  - Unique: `(plant_id, care_date, care_type)`
  - Index: `(plant_id, care_date)`
- Use ORM loader strategies: prefer `selectinload` for collections
- Batch inserts in migrations

---

## Acceptance Checklist
- Connection works
- Tables created (Core and ORM)
- CRUD and queries succeed (both ways)
- Slice + full migration done, idempotent
- Verification passes
- Export matches your Excel layout
- Optional endpoints return expected shapes

## Troubleshooting
- Connection: check `.env`, VPC/security rules, `psycopg2-binary`
- Duplicates: rely on unique key, handle `IntegrityError`
- Name inconsistencies: add normalization during migration
- Performance: add indexes early; avoid N+1 with ORM loaders
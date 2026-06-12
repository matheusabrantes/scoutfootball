# Storage Decision

## Decision

Use local SQLite for the real-data MVP development phase, with a simple repository layer that can later move to PostgreSQL.

## Rationale

- The immediate goal is provider validation and a small real-data pipeline, not production scale.
- SQLite is enough for local league/player samples, metric calculations, percentiles, and UI development.
- A repository layer keeps the app from depending on SQLite-specific behavior.
- PostgreSQL remains the production target once the source provider and data model are proven.

## Scope For This Phase

- Store provider validation metadata.
- Store small allowed sample metadata or row samples if provider terms permit.
- Store normalized league, player, player-season, and metric rows once ingestion is implemented.
- Avoid large raw provider dumps.

## Rules

- Never commit real secrets.
- Do not commit large raw API responses.
- If provider cache/storage terms are unclear, store only field names, row counts, league ids, season ids, and validation metadata.
- Keep raw provider payloads out of git unless explicitly allowed by license terms and intentionally limited.

## Future Migration

When the MVP needs hosted data:

1. Move schema to PostgreSQL.
2. Add migrations.
3. Keep provider ingestion idempotent.
4. Add ingestion run audit records.
5. Add data freshness checks.


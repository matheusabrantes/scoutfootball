# Deployment Data Strategy

Decision date: 2026-06-14

ScoutFootball currently uses historical StatsBomb Open Data plus SQLite. Raw data and generated DB files are intentionally not committed. The deployment strategy must preserve reproducibility without adding unnecessary infrastructure.

## Option A — Build-Time Ingestion

The deployment downloads StatsBomb data and builds SQLite during each deploy.

| Factor | Evaluation |
| --- | --- |
| Build duration | Poor. Full PL download took `212.771s`; aggregation and ingestion add about another minute. |
| Network reliability | Risky. GitHub raw downloads can fail transiently and would fail the deployment. |
| Storage persistence | Poor on platforms with ephemeral build/runtime filesystems. |
| Repeated downloads | Wasteful; 1.1GB StatsBomb cache would be rebuilt frequently. |
| Platform limits | Risky for Vercel/Netlify/Cloudflare style build limits; acceptable only for manual local Docker. |

Verdict: not recommended for public deployment.

## Option B — Prebuilt Release Database

Generate `scoutfootball.db` locally or in CI, upload it to object storage or a GitHub release artifact, and have the backend download it on startup or before release.

| Factor | Evaluation |
| --- | --- |
| Reproducibility | Good if the release DB is tied to a script version, source competition IDs, and checksum. |
| Versioning | Good with dated artifacts such as `scoutfootball-2026-06-14-pl-2015-2016.db`. |
| File size | Good. PL-only SQLite DB is about `7.74 MB`; raw cache is about `1.1 GB`. |
| Startup download | Simple; a small DB artifact is fast to fetch. |
| Data updates | Manual but clear: regenerate, validate, upload new DB, update checksum/env. |
| Cost | Very low; object storage or GitHub release artifacts can be free/cheap for this size. |

Verdict: best near-term strategy for this personal non-commercial project.

## Option C — PostgreSQL With Ingestion Job

Use managed PostgreSQL and run ingestion separately.

| Factor | Evaluation |
| --- | --- |
| Cost | Higher than SQLite. Managed Postgres often starts around several dollars per month. |
| Operational complexity | Higher: migrations, credentials, backups, job scheduling, connection pooling. |
| Persistence | Strong. |
| Future scaling | Best path if data grows, users write data, or concurrent traffic increases. |

Verdict: not justified yet. Keep as future migration path.

## Option D — Persistent Volume With SQLite

Deploy FastAPI in a container and attach persistent disk for SQLite and optional StatsBomb cache.

| Factor | Evaluation |
| --- | --- |
| Cost | Low on platforms with cheap disks; Render disks require paid services, Railway/Fly support volumes. |
| Backups | Must be configured. SQLite file backups are simple but easy to forget. |
| Single-instance limits | SQLite works for one backend instance; horizontal scaling is limited. |
| Platform support | Good on Render paid services, Railway volumes, Fly volumes; not suitable for ephemeral free services. |

Verdict: acceptable for a simple backend if the host supports persistent volumes cheaply.

## Recommendation

Recommended initial architecture:

1. Frontend: static Vite build on Cloudflare Pages or Vercel.
2. Backend: small Docker container on a low-cost host.
3. Data: prebuilt release SQLite DB downloaded or mounted at startup.
4. Refresh: regenerate the DB locally/CI, validate, publish a new artifact, and redeploy backend.

Preferred data model: Option B now, Option D as a practical deployment variant if the chosen backend host has cheap persistent volumes.

Do not migrate to PostgreSQL yet. The current DB is small, read-heavy, and single-writer ingestion is manual. PostgreSQL becomes justified when ScoutFootball needs automated refresh jobs, multiple seasons/leagues at larger scale, writes from users, or multi-instance backend scaling.

## Estimated Monthly Cost

Lowest-cost personal setup estimate:

- Static frontend: $0/month on Cloudflare Pages, Vercel Hobby, or Netlify Free.
- Backend container: approximately $5–$7/month on a small always-on service, or lower with usage-based platforms but more variability.
- SQLite artifact storage: $0/month if GitHub release artifacts are acceptable; object storage for a sub-10MB DB should be near-zero.

Practical estimate: $0/month for local-only; $5–$10/month for a small public backend without PostgreSQL.

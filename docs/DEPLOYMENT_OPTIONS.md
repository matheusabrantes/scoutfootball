# Deployment Options

Research date: 2026-06-14

This is a planning document only. No public deployment or paid resource was created.

## Source Notes

- Vercel Hobby is documented as free for personal projects, with Pro at $20/month. Sources: https://vercel.com/pricing and https://vercel.com/docs/plans/hobby
- Cloudflare Pages Free lists $0, 500 builds/month, 100 custom domains per project, unlimited static requests, and unlimited bandwidth. Source: https://pages.cloudflare.com/
- Netlify Free lists $0, custom domains with SSL, global CDN, and 300 credits/month. Source: https://www.netlify.com/pricing/
- Render pricing lists Hobby at $0/month plus compute, and Render docs state persistent disks are available only on paid services while free web services cannot preserve local filesystem changes. Sources: https://render.com/pricing, https://render.com/docs/disks, https://render.com/docs/free
- Railway pricing lists a free start with 30-day trial/$5 credits then low-cost usage, 0.5GB volume storage, and Railway docs describe persistent volumes. Sources: https://railway.com/pricing and https://docs.railway.com/volumes/reference
- Fly.io documents usage-based pricing and volumes at $0.15/GB/month. Sources: https://fly.io/docs/about/pricing/ and https://fly.io/docs/volumes/overview/

## Frontend Hosting

| Platform | Monthly cost | Free tier | Sleep behavior | Persistent disk | Docker support | Custom domain | Env vars | Deployment complexity | ScoutFootball fit |
| --- | ---: | --- | --- | --- | --- | --- | --- | --- | --- |
| Cloudflare Pages | $0 for static frontend | Strong free Pages tier | None for static | Not needed | No for static Pages | Yes | Yes | Low | Best low-cost static frontend fit. |
| Vercel | $0 Hobby for personal projects | Strong Hobby tier | None for static | Not needed | Framework/build oriented, not Docker-first for this use | Yes | Yes | Low | Good fit, especially if using Vercel workflow. |
| Netlify | $0 Free | Good free static tier with credits | None for static | Not needed | Build oriented, not Docker-first for this use | Yes | Yes | Low | Good fit; watch usage/credit behavior. |

Recommendation: Cloudflare Pages or Vercel for frontend. Cloudflare Pages is especially attractive for low-cost static hosting.

## Backend Hosting

| Platform | Monthly cost | Free tier | Sleep behavior | Persistent disk support | Docker support | Custom domain | Env vars | Deployment complexity | ScoutFootball fit |
| --- | ---: | --- | --- | --- | --- | --- | --- | --- | --- |
| Render | $0 hobby/free web possible; paid needed for disk | Free web service exists | Free services may sleep/ephemeral | Paid services only for disks | Yes | Yes | Yes | Low | Good if paying for a small service/disk; not for free persistent SQLite. |
| Railway | Trial/free start; then usage-based | Trial/credits | Depends on usage/project settings | Volumes supported | Yes | Yes | Yes | Low | Good developer UX; watch ongoing usage cost. |
| Fly.io | Usage-based; volume $0.15/GB/month | No strong long-term free assumption | Machines can be stopped/scaled | Volumes supported | Yes | Yes | Yes | Medium | Good technical fit for SQLite volume, but more ops-heavy. |

## Persistent Data Options

| Option | Monthly cost | Fit |
| --- | ---: | --- |
| Prebuilt SQLite artifact | $0 to near-zero | Best near-term fit. Small DB, easy versioning, no database server. |
| Persistent volume + SQLite | Low but host-dependent | Good if backend host supports cheap volume and backups. |
| Managed PostgreSQL | Usually $5+/month | Future fit; currently unnecessary. |
| Build-time ingestion | $0 infra but expensive deploy time | Poor fit because raw cache is 1.1GB and network-dependent. |

## Recommended Deployment Shape

Near-term personal release readiness:

1. Cloudflare Pages or Vercel serves the frontend.
2. A small Docker backend serves FastAPI.
3. Backend uses a prebuilt SQLite DB artifact or a mounted SQLite file on a persistent volume.
4. Data refresh remains a manual release operation until usage justifies automation.

Estimated monthly cost: $0 for frontend plus about $5–$10 for a small backend if made public. Keep PostgreSQL out of scope for now.

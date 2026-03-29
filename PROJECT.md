# Alberta Farm Finder

A free, opt-in marketplace where local Alberta farms list themselves and their products, and consumers search by product type and proximity (FB Marketplace style).

## Quick Reference

- **Stack:** Next.js, Supabase (PostgreSQL + PostGIS + Auth + Storage), Mapbox, Vercel
- **Region:** Alberta-first, architected for multi-province expansion
- **Cost target:** $0/mo at launch (free tiers), ~$50-100/mo at scale
- **Aesthetic:** Solarpunk / organic — see DESIGN.md for full details

## Core Concept

- Farmers create a profile: name, location, product tags, photos, contact info, hours
- Buyers search by location + product category, see results as cards with distance badges
- Map view with farm pins, radius slider (10-200 km), category filters
- Reviews, verified badges, seasonal availability toggles

## Key Technical Decisions

- PostGIS for geospatial distance queries (ST_DWithin, ST_Distance)
- Location stored as lat/lng; display can be town-level for farmer privacy
- Hierarchical product categories (category > subcategory) with custom tags
- Supabase handles auth, DB, storage, and realtime in one service
- SEO-friendly farm profile pages via Next.js SSR

## Project Structure

```
Alberta-Farm-Finder/
  PROJECT.md        <- This file (quick reference)
  DESIGN.md         <- Aesthetic philosophy + UI design specs
  docs/             <- Design docs, planning, style guide
  src/              <- Application source code
  database/         <- Schema migrations and seed data
```

## Phases

1. **MVP (Weeks 1-6):** DB + auth + farmer onboarding + search + map + farm profiles
2. **Community (Weeks 7-10):** Reviews, farmer dashboard, verified badges, seasonal toggles
3. **Growth (Weeks 11-16):** Messaging, alerts, province expansion, PWA

## Documents

- [Design & Plan (docx)](docs/Alberta_Farm_Finder_Design_Plan.docx) — Full product design, data model, architecture, roadmap
- [Style Guide (html)](docs/style-guide.html) — Interactive visual reference with live component samples
- [DESIGN.md](DESIGN.md) — Aesthetic philosophy and UI design specifications

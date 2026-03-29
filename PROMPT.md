# Alberta Farm Finder — Build Prompt

You are picking up an existing project plan for a local farm marketplace called Alberta Farm Finder. Before writing any code, read these files in the project root:

1. `PROJECT.md` — Quick reference: stack, concept, phases
2. `DESIGN.md` — Aesthetic philosophy and detailed UI specs (colors, typography, spacing, components)
3. `ARCHITECTURE.md` — Django app structure, models, views, URL routing, HTMX patterns, template structure

Read all three fully before starting. They are the source of truth.

---

## What This Is

A free, opt-in platform where small-scale Alberta farms list themselves and what they sell, and consumers search by product type and distance. Think Facebook Marketplace meets a farm directory — card-based results, distance badges, map view, category filters.

## Stack

- **Backend:** Django 5.x with GeoDjango (PostGIS for distance queries)
- **Frontend:** Django templates + HTMX (no React, no build step)
- **Map:** Mapbox GL JS (the one piece of real JavaScript)
- **CSS:** Single custom stylesheet, no framework — built to match DESIGN.md
- **Database:** PostgreSQL + PostGIS
- **Auth:** Django built-in auth (email + password)
- **Geocoding:** Google Maps Geocoding API (address → lat/lng on listing save)

## Aesthetic

Solarpunk. Inspired by Luke Humphris' *When Society Collapsed*. Earthy, organic, warm, community-rooted. Not corporate, not startup-y.

Key rules from DESIGN.md:
- **No plain white anywhere.** Page background is Cream (`#FDFAF3`), card surfaces are Parchment (`#F5F0E8`).
- **Everything is rounded.** Pill buttons (999px radius), 20px cards, 8px inputs. Nothing sharp.
- **Warm shadows only.** `rgba(92, 64, 51, ...)` — never cold gray shadows.
- **DM Serif Display** for headings (warm, hand-lettered feel). **DM Sans** for body (clean readability).
- **Tight spacing.** Related elements (name, location, tags, rating on a card) sit 2-4px apart, not 16-24px. Reference FB Marketplace / Airbnb card density. Do NOT over-space elements — keep things cozy and dense, not airy and sparse.
- **Warm color palette:** Moss green (`#4A6741`) for primary actions. Bark (`#5C4033`) for headings. Wheat (`#D4A853`) for highlight CTAs. See full palette in DESIGN.md.
- **Voice:** Friendly, plain, neighbourly. "Find what's growing near you" not "Discover local agricultural products."

## What to Build (MVP — Phase 1)

### Django Apps

**farms** — the core app:
- `Farm` model with PostGIS PointField, categories (M2M), photos, contact info, hours, sales channels, certifications
- `Category` model (hierarchical: parent → children)
- `FarmPhoto` model
- Search view (home page) with distance-based queries, category filtering, radius slider, keyword search
- HTMX partial responses: `_results.html` and `_card.html` for dynamic search without page reload
- Farm detail/profile page
- Farm create + edit views (login required, owner-only for edit)
- Farmer dashboard (view stats, manage listing)
- JSON endpoint for Mapbox pins (`/api/farms/map-data/`)

**reviews** — separate app:
- `Review` model (rating 1-5, text, farmer response)
- HTMX-powered review list and submission

**accounts** — user auth:
- Login, register, profile views
- Django built-in auth, nothing fancy

### Templates

- `base.html` — shared layout with nav, footer, HTMX script tag, Mapbox script on pages that need it
- `farms/search.html` — home page with search bar, category chips, radius slider, results grid, map toggle
- `farms/_results.html` — HTMX partial: grid of farm cards
- `farms/_card.html` — single farm card partial
- `farms/detail.html` — full farm profile page
- `farms/create.html` / `edit.html` — listing forms
- `farms/dashboard.html` — farmer management dashboard

### Static Files

- `css/main.css` — single stylesheet implementing everything in DESIGN.md
- `js/map.js` — Mapbox init, pin rendering from GeoJSON endpoint, pin click popups
- `js/search.js` — minimal JS for geolocation detection and radius slider output

### HTMX Patterns

- Search form: `hx-get="/api/farms/search/"` → swaps `#results`
- Category chips: `hx-get` with category param → swaps `#results`
- Radius slider: `hx-trigger="change"` → re-fetches results
- Load more: append next page of cards
- Review form: `hx-post` → swaps in updated review list

### Database

- PostgreSQL with PostGIS extension
- GIST index on Farm.location (automatic from GeoDjango PointField)
- Distance queries use `ST_DWithin` and `Distance` annotation
- Seed data: create initial categories (Meat & Poultry, Eggs, Dairy, Produce, Grains & Pulses, Honey & Bee Products, Preserves & Value-Add, Plants & Nursery, Fiber & Craft, Experiences) with subcategories

## What NOT to Do

- No React, no Vue, no frontend framework
- No Tailwind — custom CSS only
- No REST API framework (DRF) — just Django views returning HTML partials and one JSON endpoint
- No plain white (`#FFFFFF`) backgrounds anywhere
- No cold gray colors
- No sharp corners on any UI element
- Don't over-engineer auth — basic Django auth is fine for MVP
- Don't build messaging, alerts, or province expansion yet — that's Phase 2+

## Adapting from Existing Django Project

I have an existing Django project structure that this should be adapted into. Look at the existing project's settings, URL patterns, and app organization and fit the farm finder apps into that structure rather than starting from scratch. Keep existing config (database settings, middleware, etc.) and add the new apps alongside what's already there.

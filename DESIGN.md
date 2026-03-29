# Alberta Farm Finder — Design Reference

## Philosophy (Short Version)

Solarpunk, inspired by Luke Humphris' *When Society Collapsed*. A hopeful, post-corporate world where communities grow food together and share openly. This app should feel like walking into a warm farm stand on a Saturday morning — hand-lettered signs, sun on wood, baskets of produce, someone smiling and saying "the eggs came in this morning."

Not slick. Not startup-y. Not complicated. Organic, clear, human.

**Three words:** Grown, not designed.

---

## Color Palette

### Primary — Greens

| Name       | Hex       | Use                                          |
|------------|-----------|----------------------------------------------|
| Moss       | `#4A6741` | Primary actions, buttons, links, nav accents  |
| Moss Light | `#5E7D54` | Hover states for moss elements               |
| Fern       | `#7BA05B` | Verified badges, positive indicators         |
| Sage       | `#A3B899` | Focus rings, secondary borders, input accents |
| Meadow     | `#D4E2C8` | Product tags, light backgrounds, section tints|

### Secondary — Earth Tones

| Name       | Hex       | Use                                          |
|------------|-----------|----------------------------------------------|
| Bark       | `#5C4033` | Headings, farm names, strong text            |
| Soil       | `#8B6F4E` | Subheadings, secondary labels, distance text |
| Wheat      | `#D4A853` | Highlight CTA ("List Your Farm"), star ratings|
| Terracotta | `#C67B5C` | Sparingly — warm accents, alerts, emphasis   |
| Sun        | `#E8B931` | Star icons, seasonal badges, celebration moments|

### Neutrals

| Name      | Hex       | Use                                           |
|-----------|-----------|-----------------------------------------------|
| Cream     | `#FDFAF3` | Page background — NEVER pure white            |
| Parchment | `#F5F0E8` | Card surfaces, card hover states, note backgrounds, insets |
| Charcoal  | `#2C2C2C` | Body text                                     |
| Stone     | `#6B6B6B` | Secondary body text, nav links                |
| Mist      | `#B8B8AA` | Placeholders, timestamps, meta text           |
| Border    | `#E5DDD0` | All borders — soft, warm, never harsh gray    |

### Rules

- Page background is always Cream, never `#FFFFFF`
- Cards use Parchment — no plain white surfaces anywhere in the app
- Never use cold grays (`#CCC`, `#999`, etc.) — all grays skew warm
- Terracotta and Sun are accent-only — never dominant
- If adding a new color, ask: "does this feel like it grew out of soil?"

---

## Typography

### Fonts

| Role     | Font              | Weight     | Fallback          |
|----------|-------------------|------------|--------------------|
| Headings | DM Serif Display  | 400        | Georgia, serif     |
| Body     | DM Sans           | 400, 500, 600 | system-ui, sans-serif |

### Scale

| Element          | Font             | Size   | Weight | Color    | Notes                    |
|------------------|------------------|--------|--------|----------|--------------------------|
| Page title       | DM Serif Display | 2.4rem | 400    | Bark     |                          |
| Section heading  | DM Serif Display | 1.5rem | 400    | Moss     | Border-bottom in Meadow  |
| Card farm name   | DM Serif Display | 1.15rem| 400    | Bark     |                          |
| Body text        | DM Sans          | 0.95rem| 400    | Charcoal | Line-height 1.6–1.7     |
| Secondary text   | DM Sans          | 0.85rem| 400    | Stone    |                          |
| Meta / timestamps| DM Sans          | 0.8rem | 400    | Mist     |                          |
| Tags / labels    | DM Sans          | 0.75rem| 600    | Varies   | Uppercase, letter-spacing 0.06–0.08em |
| Nav links        | DM Sans          | 0.85rem| 500    | Stone    | Moss on hover            |

### Rules

- Headings are always DM Serif Display — this gives the whole app its warm, hand-lettered personality
- Body is always DM Sans — clean readability, no fuss
- Never use all-caps on headings. Only tags/labels get uppercase treatment
- Keep line-height generous (1.6 minimum for body text)

---

## Shape Language

Everything is rounded. Nothing is sharp. This is the single most important visual rule.

| Element        | Border Radius |
|----------------|---------------|
| Buttons        | `999px` (pill) |
| Cards          | `20px`         |
| Input fields   | `8px`          |
| Tags / chips   | `999px` (pill) |
| Modals         | `20px`         |
| Tooltips       | `12px`         |
| Images in cards| `0` top, inherits card radius |
| Avatar circles | `50%`          |

---

## Shadows

All shadows use warm brown tinting, never cold `rgba(0,0,0,...)`.

| State    | Shadow                                    |
|----------|-------------------------------------------|
| Default  | `0 2px 8px rgba(92, 64, 51, 0.08)`       |
| Hover    | `0 8px 24px rgba(92, 64, 51, 0.12)`      |
| Elevated | `0 4px 16px rgba(92, 64, 51, 0.10)`      |
| Focus    | `0 0 0 3px rgba(163, 184, 153, 0.25)` (sage glow) |

---

## Spacing

Use a consistent 8px base grid. Keep things cozy — elements should feel related and grouped, not floating apart on a vast empty page.

| Token    | Value | Use                              |
|----------|-------|----------------------------------|
| `xs`     | 4px   | Tight gaps (icon to text)        |
| `sm`     | 8px   | Tag gaps, inner padding          |
| `md`     | 12px  | Card inner padding, paragraph spacing |
| `lg`     | 16px  | Card body padding, between related sections |
| `xl`     | 24px  | Between distinct sections        |
| `2xl`    | 40px  | Page-level top/bottom margins    |

**IMPORTANT — Anti-float rule:** Claude (the AI building this) has a tendency to over-space elements. Every gap should feel intentional and tight. Related things (a farm name and its location, a tag row and a rating) should sit close together — 4-8px, not 16-24px. Only separate *unrelated* groups with larger gaps. Think of a well-designed mobile app, not a sparse landing page. Cards should feel full and dense with information, not airy. If something looks like it's drifting apart, close the gap.

Reference density: look at how FB Marketplace, Airbnb, or Kijiji pack their cards — photo, title, price, location, meta all sit tight together with minimal internal spacing. That's the target density.

---

## UI Components

### Buttons

| Variant    | Background  | Text Color | Border          | Use                          |
|------------|-------------|------------|-----------------|------------------------------|
| Primary    | Moss        | White      | None            | Main actions (Search, Save)  |
| Secondary  | Transparent | Moss       | 1.5px Sage      | Alternate actions (View Map) |
| Warm CTA   | Wheat       | Bark       | None            | Farmer-facing CTAs (List Your Farm) |
| Ghost      | Transparent | Soil       | None            | Tertiary actions (Learn more)|

Hover: Primary lifts 1px + deeper shadow. Secondary fills with Meadow. Warm brightens slightly.
All buttons are pill-shaped (`border-radius: 999px`). Padding: `10px 22px`. Font: DM Sans 500 at 0.9rem.

### Cards (Farm Listing)

The primary browse element. Structure top to bottom:

1. **Photo area** — 180px tall, full width, covers top of card. If no photo, show a gradient using greens/earth tones with a faint emoji placeholder.
2. **Distance badge** — Positioned top-right of photo. White pill with backdrop blur. Shows "12 km" in Soil, DM Sans 600 at 0.75rem.
3. **Farm name** — DM Serif Display, Bark, 1.15rem.
4. **Location** — Town + province. Mist, 0.8rem.
5. **Product tags** — Row of Meadow-green pills. 2-3 max visible, "+N more" if overflow.
6. **Rating** — Wheat stars + Soil text. "4.9 (23)".

Card hover: lift 3px + shadow deepens. Transition 0.25s ease.
Card padding: `12px` on sides and bottom, `0` on photo top. Keep internal spacing tight — 2-4px between name/location/tags/rating, not 8-16px.

### Search Bar

The hero element of the home page. Centered, prominent, inviting.

- Pill-shaped container (border-radius 999px)
- White background, 1.5px Border color, elevated shadow
- Input field fills left side, no visible border
- Search button (Primary style) docked on right inside the pill
- Placeholder: "Search for eggs, honey, beef near Lacombe..."
- Max width ~600px, centered

### Tags / Chips

| Type      | Background | Text Color | Border     | Example          |
|-----------|------------|------------|------------|------------------|
| Product   | Meadow     | Moss       | None       | "Eggs"           |
| Distance  | Parchment  | Soil       | 1px Border | "12 km away"     |
| Season    | `#FFF3D6`  | `#8B6914`  | None       | "In Season"      |
| Verified  | `#E8F4EA`  | Moss       | None       | "✓ Verified"     |
| Category filter | White | Charcoal  | 1px Border | "Honey" (clickable) |
| Category active | Moss  | White     | None       | "Honey" (selected)|

### Form Inputs

- Rounded corners (8px)
- Border: 1.5px in Border color
- Focus: border transitions to Sage + sage glow shadow
- Labels: DM Sans 600, 0.8rem, Bark color, above the input
- Placeholders: Mist color
- Padding: 10px 14px

### Radius Slider

- Track: gradient from Sage to Meadow (left to right)
- Thumb: 20px circle, Moss fill, 3px white border, subtle shadow
- Label above shows current value in Moss bold ("50 km")

### Navigation Bar

- White background, subtle bottom border or shadow
- Logo left: "Farm" in DM Serif Display Moss + "Finder" in Wheat
- Nav links right: DM Sans 500, Stone, Moss on hover
- "List Your Farm" button: Warm CTA variant, slightly smaller padding
- Sticky on scroll

### Map View

- Mapbox with a warm/muted custom style (avoid the default blue-heavy look)
- Farm pins: Moss-colored circles with white icon, or small leaf/sprout icon
- Selected pin: Scales up + Wheat ring
- Info popup on pin click: mini farm card (photo, name, distance, top tags)
- Cluster circles: Sage background with Moss count number

### Farm Profile Page

Top to bottom layout:

1. **Photo gallery** — Horizontal carousel or grid. Rounded corners matching card radius.
2. **Header row** — Farm name (DM Serif, Bark, large) + verified badge + rating. Distance badge + "Get Directions" button.
3. **Product section** — Grid of product tags with availability indicators (in-season / seasonal / year-round).
4. **About** — Farm description in body text. Certifications as tags.
5. **Contact** — Card with phone, email, website, social. Only what the farmer chose to show.
6. **Hours** — Structured display. Seasonal notes in italics.
7. **Reviews** — Star breakdown bar + individual review cards.

### Empty States

When there are no results or content is missing, use:
- Illustration: simple line-art style (hand-drawn feel) in Sage/Mist tones
- Friendly copy: "No farms found nearby — try widening your search radius" not "No results"
- A gentle suggestion or action button

### Loading States

- Skeleton screens, not spinners
- Skeleton shapes match the content they replace (card placeholders, text lines)
- Skeleton fill: subtle pulse animation between Parchment and Cream
- Keep it calm — no aggressive flashing

---

## Animation & Motion

Everything moves gently. Nothing bounces, flashes, or demands attention.

| Interaction     | Duration | Easing    | Effect                        |
|-----------------|----------|-----------|-------------------------------|
| Card hover      | 0.25s    | ease      | translateY(-3px) + shadow     |
| Button hover    | 0.2s     | ease      | translateY(-1px) + shadow/fill|
| Page transitions| 0.3s     | ease-out  | Fade or gentle slide          |
| Skeleton pulse  | 1.5s     | ease-in-out| Background opacity cycle     |
| Map pin select  | 0.2s     | ease      | Scale up 1.2x                 |
| Modal open      | 0.25s    | ease-out  | Fade + slide up from 10px     |

---

## Iconography

- Style: Line icons only — never filled/solid
- Weight: 1.5-2px stroke
- Consider a hand-drawn icon set to match the organic feel (like Phosphor icons "thin" variant or custom)
- Color: inherits from context (Moss for actions, Stone for nav, Mist for decorative)
- Size: 20px default, 16px inline with text

---

## Photography Guidelines

Farm photos are a huge part of the experience. Guidelines for farmer uploads:

- Encourage natural light, outdoor shots
- Consider a subtle warm-tone CSS filter on all farm photos for consistency: `filter: saturate(0.95) brightness(1.02) sepia(0.05)`
- Placeholder gradient for farms without photos: `linear-gradient(135deg, #B5C99A, #87A96B)` with a faint plant emoji

---

## Responsive Behavior

| Breakpoint | Layout                                          |
|------------|--------------------------------------------------|
| Desktop (1024px+) | 3-column card grid, sidebar filters, map beside list |
| Tablet (768-1023px) | 2-column card grid, filters collapse to dropdown, map full-width toggle |
| Mobile (<768px) | Single column cards, bottom sheet filters, map as separate tab |

Search bar is always centered and prominent across all breakpoints.
Nav collapses to hamburger on mobile with slide-out drawer.

---

## Voice & Copy Guidelines

Write like you're talking to a neighbour over the fence.

| Do                                | Don't                                    |
|-----------------------------------|------------------------------------------|
| "Find what's growing near you"    | "Discover local agricultural products"   |
| "List your farm"                  | "Create a vendor account"                |
| "8 km away"                       | "8.0 kilometers from your location"      |
| "Fresh eggs from Sunridge Farm"   | "Product listing: Eggs (SKU-4421)"       |
| "Last updated 3 days ago"         | "Modified: 2026-03-26T14:22:00Z"         |
| "No farms nearby — try a wider search" | "Error: 0 results returned"         |
| "What are you looking for?"       | "Enter search query"                     |

Keep it warm, short, and human. If copy sounds like it came from a SaaS template, rewrite it.

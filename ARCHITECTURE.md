# Alberta Farm Finder — Site Architecture

## Stack

| Layer       | Technology                     | Why                                              |
|-------------|--------------------------------|--------------------------------------------------|
| Backend     | Django 5.x                     | Adapting from existing project                   |
| Database    | PostgreSQL + PostGIS           | Geospatial queries for distance search           |
| Frontend    | Django templates + HTMX        | No build step, dynamic UX with HTML attributes   |
| Map         | Mapbox GL JS (vanilla JS)      | Interactive map, the one place we need real JS    |
| CSS         | Single stylesheet (no framework)| Custom styles matching DESIGN.md                 |
| Auth        | Django built-in auth           | Email + password, extend later if needed         |
| Storage     | Django + S3-compatible (later) | Farm photos; local FileField for dev             |
| Geocoding   | Google Maps Geocoding API      | Address to lat/lng on farm creation              |
| Hosting     | TBD (Railway, Render, VPS)     | Django-friendly hosts with PostGIS support       |

## Why HTMX

HTMX lets us do dynamic partial-page updates without writing a JS framework. Examples:
- Searching farms → HTMX swaps in a new results partial without full page reload
- Changing filters/radius → HTMX re-fetches the filtered results
- Loading more cards → HTMX appends the next page
- Toggling map/list view → HTMX swaps the content area

The only real JavaScript is the Mapbox map initialization and pin interaction. Everything else stays in Django templates.

---

## Django App Structure

```
alberta_farm_finder/          # Django project root
├── manage.py
├── config/                   # Project settings
│   ├── settings.py
│   ├── urls.py               # Root URL conf
│   └── wsgi.py
│
├── farms/                    # Core app — farm listings
│   ├── models.py             # Farm, Category, Photo, Hours
│   ├── views.py              # List, detail, create, edit, dashboard
│   ├── urls.py               # /farms/, /farms/<slug>/, /farms/new/
│   ├── forms.py              # Farm creation/edit forms
│   ├── admin.py              # Django admin for moderation
│   └── templates/
│       └── farms/
│           ├── search.html           # Home/search page
│           ├── _card.html            # Single farm card partial (HTMX target)
│           ├── _results.html         # Results grid partial (HTMX target)
│           ├── detail.html           # Farm profile page
│           ├── create.html           # Farmer listing form
│           ├── edit.html             # Edit listing
│           └── dashboard.html        # Farmer dashboard
│
├── reviews/                  # Reviews app
│   ├── models.py             # Review, FarmerResponse
│   ├── views.py
│   ├── urls.py               # /farms/<slug>/reviews/
│   └── templates/
│       └── reviews/
│           ├── _list.html            # Reviews list partial
│           └── _form.html            # Review submission partial
│
├── accounts/                 # User auth & profiles
│   ├── models.py             # UserProfile (extends User)
│   ├── views.py              # Login, register, profile
│   ├── urls.py               # /login/, /register/, /profile/
│   └── templates/
│       └── accounts/
│           ├── login.html
│           ├── register.html
│           └── profile.html
│
├── templates/                # Project-level shared templates
│   ├── base.html             # Base layout (nav, footer, HTMX/Mapbox scripts)
│   ├── _nav.html             # Navigation partial
│   ├── _footer.html          # Footer partial
│   └── _messages.html        # Django messages (flash notifications)
│
├── static/
│   ├── css/
│   │   └── main.css          # Single stylesheet (mirrors DESIGN.md)
│   ├── js/
│   │   ├── map.js            # Mapbox initialization + farm pins
│   │   └── search.js         # Minimal JS for radius slider, geolocation
│   └── img/                  # Static assets (logo, fallback images)
│
└── media/                    # User uploads (farm photos)
```

---

## Models

### Farm

```python
from django.contrib.gis.db import models as gis_models

class Farm(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='farms')
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    # Location
    location = gis_models.PointField(geography=True, srid=4326)
    address_display = models.CharField(max_length=300)  # "Lacombe, AB" (public)
    address_full = models.CharField(max_length=500)      # Full address (private, for geocoding)
    province = models.CharField(max_length=50, default='Alberta')

    # Details
    categories = models.ManyToManyField('Category', related_name='farms')
    sales_channels = models.JSONField(default=list)  # ["farm_gate", "u_pick", "delivery", "farmers_market"]
    certifications = models.JSONField(default=list)   # ["organic", "grass_fed", "free_range"]
    contact_phone = models.CharField(max_length=20, blank=True)
    contact_email = models.EmailField(blank=True)
    contact_website = models.URLField(blank=True)
    hours = models.JSONField(default=dict, blank=True)

    # Status
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def average_rating(self):
        return self.reviews.aggregate(avg=models.Avg('rating'))['avg'] or 0

    def review_count(self):
        return self.reviews.count()
```

### Category

```python
class Category(models.Model):
    name = models.CharField(max_length=100)        # "Eggs"
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey('self', null=True, blank=True,
                               on_delete=models.CASCADE, related_name='children')
    icon = models.CharField(max_length=10, blank=True)  # Emoji or icon class

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ['name']
```

### FarmPhoto

```python
class FarmPhoto(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='farm_photos/%Y/%m/')
    is_primary = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
```

### Review

```python
class Review(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()  # 1-5
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    farmer_response = models.TextField(blank=True)
    farmer_responded_at = models.DateTimeField(null=True, blank=True)
```

---

## URL Structure

```
/                                   → Search/home page (farms:search)
/farms/<slug>/                      → Farm profile (farms:detail)
/farms/new/                         → Create listing (farms:create) [login required]
/farms/<slug>/edit/                 → Edit listing (farms:edit) [owner only]
/farms/<slug>/reviews/              → Reviews list
/farms/<slug>/reviews/new/          → Submit review [login required]
/dashboard/                         → Farmer dashboard (farms:dashboard) [login required]
/login/                             → Login
/register/                          → Register
/profile/                           → User profile settings
/api/farms/search/                  → HTMX endpoint: returns _results.html partial
/api/farms/map-data/                → JSON endpoint: farm pins for Mapbox [{lat, lng, name, slug, ...}]
```

The `/api/` prefix is for HTMX and JS endpoints — they return HTML partials or JSON, not full pages.

---

## Key Views

### Search (Home Page)

```python
# farms/views.py
from django.contrib.gis.measure import D
from django.contrib.gis.geos import Point

def search(request):
    """Main search page. Also handles HTMX partial responses."""
    lat = request.GET.get('lat')
    lng = request.GET.get('lng')
    category = request.GET.get('category')
    radius = int(request.GET.get('radius', 50))
    q = request.GET.get('q', '')

    farms = Farm.objects.filter(is_active=True)

    if lat and lng:
        user_point = Point(float(lng), float(lat), srid=4326)
        farms = farms.filter(
            location__distance_lte=(user_point, D(km=radius))
        ).annotate(
            distance=Distance('location', user_point)
        ).order_by('distance')

    if category:
        farms = farms.filter(categories__slug=category)

    if q:
        farms = farms.filter(
            models.Q(name__icontains=q) |
            models.Q(description__icontains=q) |
            models.Q(categories__name__icontains=q)
        ).distinct()

    categories = Category.objects.filter(parent=None)

    # HTMX partial response
    if request.headers.get('HX-Request'):
        return render(request, 'farms/_results.html', {'farms': farms})

    return render(request, 'farms/search.html', {
        'farms': farms,
        'categories': categories,
        'selected_category': category,
        'radius': radius,
        'query': q,
    })
```

### Map Data (JSON for Mapbox)

```python
from django.http import JsonResponse

def map_data(request):
    """Returns farm locations as JSON for Mapbox pins."""
    farms = Farm.objects.filter(is_active=True).only(
        'name', 'slug', 'location', 'address_display'
    ).prefetch_related('categories', 'photos')

    # Apply same filters as search view...

    features = [{
        'type': 'Feature',
        'geometry': {
            'type': 'Point',
            'coordinates': [farm.location.x, farm.location.y],
        },
        'properties': {
            'name': farm.name,
            'slug': farm.slug,
            'address': farm.address_display,
            'categories': [c.name for c in farm.categories.all()[:3]],
            'photo': farm.photos.filter(is_primary=True).first().image.url if farm.photos.exists() else None,
            'rating': farm.average_rating(),
        }
    } for farm in farms]

    return JsonResponse({'type': 'FeatureCollection', 'features': features})
```

---

## Template Structure

### base.html (skeleton)

```
<!DOCTYPE html>
<html>
<head>
    <link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@400;500;600" rel="stylesheet">
    <link rel="stylesheet" href="{% static 'css/main.css' %}">
</head>
<body>
    {% include '_nav.html' %}
    {% include '_messages.html' %}

    <main>{% block content %}{% endblock %}</main>

    {% include '_footer.html' %}

    <!-- HTMX (one script, no build step) -->
    <script src="https://unpkg.com/htmx.org@2.0.0"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>
```

### search.html (home page, simplified)

```html
{% extends 'base.html' %}

{% block content %}
<section class="search-hero">
    <h1>Find what's growing near you</h1>
    <form class="search-bar"
          hx-get="/api/farms/search/"
          hx-target="#results"
          hx-trigger="submit, change from:.filter-input">
        <input type="text" name="q" placeholder="Search for eggs, honey, beef...">
        <input type="hidden" name="lat" id="user-lat">
        <input type="hidden" name="lng" id="user-lng">
        <button type="submit">Search</button>
    </form>
</section>

<section class="category-chips">
    {% for cat in categories %}
    <button class="chip {% if cat.slug == selected_category %}active{% endif %}"
            hx-get="/api/farms/search/?category={{ cat.slug }}"
            hx-target="#results">
        {{ cat.icon }} {{ cat.name }}
    </button>
    {% endfor %}
</section>

<section class="filters">
    <label>Within <output id="radius-val">{{ radius }}</output> km</label>
    <input type="range" name="radius" min="10" max="200" value="{{ radius }}"
           class="filter-input"
           oninput="document.getElementById('radius-val').value = this.value">
</section>

<div class="view-toggle">
    <button class="active">List</button>
    <button hx-get="/api/farms/search/?view=map" hx-target="#results">Map</button>
</div>

<div id="results">
    {% include 'farms/_results.html' %}
</div>
{% endblock %}
```

### _card.html (single farm card)

```html
<a href="{% url 'farms:detail' farm.slug %}" class="farm-card">
    <div class="card-img">
        {% if farm.primary_photo %}
        <img src="{{ farm.primary_photo.image.url }}" alt="{{ farm.name }}">
        {% else %}
        <div class="card-img-placeholder"></div>
        {% endif %}
        {% if distance %}
        <span class="distance-badge">{{ distance.km|floatformat:0 }} km</span>
        {% endif %}
    </div>
    <div class="card-body">
        <h3 class="card-name">{{ farm.name }}</h3>
        <p class="card-location">{{ farm.address_display }}</p>
        <div class="card-tags">
            {% for cat in farm.categories.all|slice:":3" %}
            <span class="tag tag-product">{{ cat.name }}</span>
            {% endfor %}
        </div>
        <div class="card-rating">
            <span class="stars">{{ farm.star_display }}</span>
            {{ farm.average_rating|floatformat:1 }} ({{ farm.review_count }})
        </div>
    </div>
</a>
```

---

## HTMX Patterns Used

| Pattern                  | How                                                          |
|--------------------------|--------------------------------------------------------------|
| Search results           | `hx-get` on form submit → swaps `#results` with partial     |
| Category filter          | `hx-get` on chip click → re-fetches results with filter     |
| Radius change            | `hx-trigger="change"` on slider → re-fetches results        |
| Load more                | `hx-get` with `?page=N` on "Load more" button → appends     |
| Review submission        | `hx-post` on review form → swaps in updated review list     |
| Seasonal toggle (farmer) | `hx-patch` on toggle → updates single product availability  |

---

## Map Integration (map.js)

The map is the one piece that needs real JavaScript:

```javascript
// static/js/map.js
// Initializes Mapbox, fetches /api/farms/map-data/, renders pins
// Pin click opens a mini card popup
// Syncs with search filters via URL params
```

Map gets the same filter params as the search view, so switching between list and map view shows the same farms.

---

## Geocoding Flow

When a farmer creates or edits a listing:

1. Farmer enters address in form
2. On save, backend calls Google Geocoding API → gets lat/lng
3. Stores `Point(lng, lat)` in the `location` field
4. Generates `address_display` from geocoding result (town + province only, for privacy)
5. Stores `address_full` privately (never exposed to public)

---

## Database Notes

### PostGIS Setup

```sql
CREATE EXTENSION postgis;
```

Django uses `django.contrib.gis` (GeoDjango). Settings:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'farm_finder',
        ...
    }
}

INSTALLED_APPS = [
    'django.contrib.gis',
    ...
]
```

### Key Indexes

```python
# On the Farm model
class Meta:
    indexes = [
        models.Index(fields=['is_active', '-updated_at']),
        models.Index(fields=['province']),
    ]
# PostGIS automatically indexes the PointField (GIST index)
```

---

## Auth Flow

| Action              | Access          | Notes                              |
|---------------------|-----------------|-------------------------------------|
| Browse / search     | Public          | No login needed                    |
| View farm profile   | Public          | No login needed                    |
| Create listing      | Login required  | Becomes farm owner                 |
| Edit listing        | Owner only      | `@login_required` + ownership check|
| Dashboard           | Login required  | Shows only your farms              |
| Submit review       | Login required  | Can't review own farm              |
| Respond to review   | Farm owner only |                                     |

---

## Deployment Checklist (When Ready)

- [ ] PostgreSQL + PostGIS on host
- [ ] `collectstatic` for CSS/JS/images
- [ ] S3-compatible storage for media (farm photos)
- [ ] Google Geocoding API key in env vars
- [ ] Mapbox access token in env vars
- [ ] `ALLOWED_HOSTS`, `DEBUG=False`, `SECRET_KEY` in env
- [ ] HTTPS via host or Cloudflare
- [ ] Django admin for category management and moderation

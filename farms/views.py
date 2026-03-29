from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404
from django.db import models
from django.contrib import messages

from .models import Farm, Category, FarmPhoto, FarmersMarket, FarmProduct
from .forms import FarmForm, FarmPhotoForm


FARMS_PER_PAGE = 12


def search(request):
    lat = request.GET.get('lat')
    lng = request.GET.get('lng')
    category = request.GET.get('category')
    radius = int(request.GET.get('radius', 50))
    q = request.GET.get('q', '')
    sort = request.GET.get('sort', 'distance')
    page = int(request.GET.get('page', 1))

    farms = Farm.objects.filter(is_active=True).prefetch_related('categories', 'photos')

    if category:
        farms = farms.filter(categories__slug=category)

    if q:
        farms = farms.filter(
            models.Q(name__icontains=q) |
            models.Q(description__icontains=q) |
            models.Q(categories__name__icontains=q)
        ).distinct()

    farm_list = list(farms)
    has_location = bool(lat and lng)

    if has_location:
        user_lat, user_lng = float(lat), float(lng)
        for farm in farm_list:
            farm.distance_km = farm.distance_to(user_lat, user_lng)
        farm_list = [f for f in farm_list if f.distance_km is not None and f.distance_km <= radius]

    # Sort
    if sort == 'rating':
        farm_list.sort(key=lambda f: f.average_rating(), reverse=True)
    elif sort == 'newest':
        farm_list.sort(key=lambda f: f.created_at, reverse=True)
    elif sort == 'name':
        farm_list.sort(key=lambda f: f.name.lower())
    elif has_location:
        farm_list.sort(key=lambda f: f.distance_km)

    total_count = len(farm_list)

    # Paginate
    start = (page - 1) * FARMS_PER_PAGE
    end = start + FARMS_PER_PAGE
    farm_page = farm_list[start:end]
    has_more = end < total_count

    categories = Category.objects.filter(parent=None)

    ctx = {
        'farms': farm_page,
        'total_count': total_count,
        'has_location': has_location,
        'has_more': has_more,
        'next_page': page + 1,
        'sort': sort,
    }

    if request.headers.get('HX-Request'):
        # If loading more, just return cards to append
        if request.GET.get('append'):
            return render(request, 'farms/_cards_page.html', ctx)
        return render(request, 'farms/_results.html', ctx)

    ctx.update({
        'categories': categories,
        'selected_category': category,
        'radius': radius,
        'query': q,
    })
    return render(request, 'farms/search.html', ctx)


def farm_detail(request, slug):
    farm = get_object_or_404(
        Farm.objects.prefetch_related('categories', 'photos', 'reviews__author', 'products__category', 'markets'),
        slug=slug, is_active=True,
    )
    return render(request, 'farms/detail.html', {'farm': farm})


@login_required
def farm_create(request):
    if request.method == 'POST':
        form = FarmForm(request.POST)
        if form.is_valid():
            farm = form.save(commit=False)
            farm.owner = request.user
            farm.save()
            form.save_m2m()

            if request.FILES.get('photo'):
                FarmPhoto.objects.create(farm=farm, image=request.FILES['photo'], is_primary=True)

            messages.success(request, 'Your farm has been listed!')
            return redirect('farms:detail', slug=farm.slug)
    else:
        form = FarmForm()

    return render(request, 'farms/create.html', {
        'form': form,
        'parent_categories': Category.objects.filter(parent=None),
    })


@login_required
def farm_edit(request, slug):
    farm = get_object_or_404(Farm, slug=slug)
    if farm.owner != request.user:
        raise Http404

    if request.method == 'POST':
        form = FarmForm(request.POST, instance=farm)
        if form.is_valid():
            form.save()

            if request.FILES.get('photo'):
                FarmPhoto.objects.create(
                    farm=farm, image=request.FILES['photo'],
                    is_primary=not farm.photos.exists(),
                )

            messages.success(request, 'Farm listing updated!')
            return redirect('farms:detail', slug=farm.slug)
    else:
        form = FarmForm(instance=farm)

    return render(request, 'farms/edit.html', {
        'form': form,
        'farm': farm,
        'parent_categories': Category.objects.filter(parent=None),
    })


@login_required
def dashboard(request):
    farms = Farm.objects.filter(owner=request.user).prefetch_related('photos', 'reviews', 'products')
    return render(request, 'farms/dashboard.html', {'farms': farms})


@login_required
def manage_products(request, slug):
    """HTMX endpoint for sellers to add/toggle product availability."""
    farm = get_object_or_404(Farm, slug=slug)
    if farm.owner != request.user:
        raise Http404

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'add':
            name = request.POST.get('product_name', '').strip()
            cat_id = request.POST.get('category_id')
            price_note = request.POST.get('price_note', '').strip()
            is_seasonal = request.POST.get('is_seasonal') == 'on'
            season_note = request.POST.get('season_note', '').strip()
            if name and cat_id:
                cat = get_object_or_404(Category, id=cat_id)
                FarmProduct.objects.create(
                    farm=farm, category=cat, name=name,
                    price_note=price_note, is_seasonal=is_seasonal,
                    season_note=season_note,
                )

        elif action == 'toggle':
            product_id = request.POST.get('product_id')
            product = get_object_or_404(FarmProduct, id=product_id, farm=farm)
            product.is_available = not product.is_available
            product.save()

        elif action == 'delete':
            product_id = request.POST.get('product_id')
            FarmProduct.objects.filter(id=product_id, farm=farm).delete()

    products = farm.products.select_related('category').all()
    categories = Category.objects.all()

    ctx = {
        'farm': farm,
        'products': products,
        'categories': categories,
    }

    # HTMX partial vs full page
    if request.headers.get('HX-Request'):
        return render(request, 'farms/_products_manage.html', ctx)
    return render(request, 'farms/products.html', ctx)


# ---- Farmers Markets ----

def market_list(request):
    markets = FarmersMarket.objects.filter(is_active=True).prefetch_related('vendors')
    return render(request, 'farms/markets.html', {'markets': markets})


def market_detail(request, slug):
    market = get_object_or_404(
        FarmersMarket.objects.prefetch_related('vendors__categories', 'vendors__photos'),
        slug=slug, is_active=True,
    )
    user_farms = []
    if request.user.is_authenticated:
        user_farms = Farm.objects.filter(owner=request.user, is_active=True)
    return render(request, 'farms/market_detail.html', {
        'market': market,
        'user_farms': user_farms,
    })


@login_required
def market_join(request, slug):
    """Add or remove a farm from a market."""
    market = get_object_or_404(FarmersMarket, slug=slug, is_active=True)
    farm_id = request.POST.get('farm_id')
    action = request.POST.get('action', 'join')
    farm = get_object_or_404(Farm, id=farm_id, owner=request.user)

    if action == 'leave':
        market.vendors.remove(farm)
        messages.success(request, f'{farm.name} removed from {market.name}.')
    else:
        market.vendors.add(farm)
        messages.success(request, f'{farm.name} is now a vendor at {market.name}!')

    return redirect('farms:market_detail', slug=slug)


def map_data(request):
    farms = Farm.objects.filter(is_active=True).prefetch_related('categories', 'photos')

    category = request.GET.get('category')
    q = request.GET.get('q', '')

    if category:
        farms = farms.filter(categories__slug=category)
    if q:
        farms = farms.filter(
            models.Q(name__icontains=q) |
            models.Q(description__icontains=q) |
            models.Q(categories__name__icontains=q)
        ).distinct()

    features = []

    # Farm pins
    for farm in farms:
        if farm.latitude is None or farm.longitude is None:
            continue
        photo = farm.primary_photo
        features.append({
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [farm.longitude, farm.latitude],
            },
            'properties': {
                'type': 'farm',
                'name': farm.name,
                'slug': farm.slug,
                'address': farm.address_display,
                'categories': [c.name for c in farm.categories.all()[:3]],
                'photo': photo.image.url if photo else None,
                'rating': farm.average_rating(),
                'reviewCount': farm.review_count(),
            }
        })

    # Market pins (golden, different style)
    markets = FarmersMarket.objects.filter(is_active=True)
    for market in markets:
        if market.latitude is None or market.longitude is None:
            continue
        features.append({
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [market.longitude, market.latitude],
            },
            'properties': {
                'type': 'market',
                'name': market.name,
                'slug': market.slug,
                'address': market.address_display,
                'categories': [],
                'photo': None,
                'next_date': market.next_date.strftime('%b %d') if market.next_date else None,
                'vendor_count': market.vendor_count(),
                'schedule': market.schedule_display,
            }
        })

    return JsonResponse({'type': 'FeatureCollection', 'features': features})

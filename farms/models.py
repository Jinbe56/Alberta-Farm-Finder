import math
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey(
        'self', null=True, blank=True,
        on_delete=models.CASCADE, related_name='children'
    )
    icon = models.CharField(max_length=10, blank=True)

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Farm(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='farms')
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    # Location — FloatFields for SQLite; swap to PointField when PostGIS is available
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    address_display = models.CharField(max_length=300, blank=True)
    address_full = models.CharField(max_length=500, blank=True)
    province = models.CharField(max_length=50, default='Alberta')

    categories = models.ManyToManyField(Category, related_name='farms', blank=True)
    sales_channels = models.JSONField(default=list, blank=True)
    certifications = models.JSONField(default=list, blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    contact_email = models.EmailField(blank=True)
    contact_website = models.URLField(blank=True)
    hours = models.JSONField(default=dict, blank=True)

    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['is_active', '-updated_at']),
            models.Index(fields=['province']),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def average_rating(self):
        avg = self.reviews.aggregate(avg=models.Avg('rating'))['avg']
        return round(avg, 1) if avg else 0

    def review_count(self):
        return self.reviews.count()

    @property
    def primary_photo(self):
        return self.photos.filter(is_primary=True).first() or self.photos.first()

    @property
    def star_display(self):
        rating = self.average_rating()
        full = int(rating)
        half = 1 if rating - full >= 0.5 else 0
        empty = 5 - full - half
        return '★' * full + ('½' if half else '') + '☆' * empty

    def distance_to(self, lat, lng):
        """Haversine distance in km — SQLite fallback for PostGIS ST_Distance."""
        if self.latitude is None or self.longitude is None:
            return None
        R = 6371
        dlat = math.radians(lat - self.latitude)
        dlng = math.radians(lng - self.longitude)
        a = (math.sin(dlat / 2) ** 2 +
             math.cos(math.radians(self.latitude)) *
             math.cos(math.radians(lat)) *
             math.sin(dlng / 2) ** 2)
        return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


class FarmProduct(models.Model):
    """What a farm currently has available for sale."""
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    is_available = models.BooleanField(default=True)
    is_seasonal = models.BooleanField(default=False)
    season_note = models.CharField(max_length=200, blank=True)
    price_note = models.CharField(max_length=200, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_available', 'name']

    def __str__(self):
        status = 'Available' if self.is_available else 'Unavailable'
        return f"{self.name} ({status})"


class FarmersMarket(models.Model):
    """A recurring market where multiple farms sell together."""
    FREQUENCY_CHOICES = [
        ('weekly', 'Weekly'),
        ('biweekly', 'Every two weeks'),
        ('monthly', 'Monthly'),
        ('seasonal', 'Seasonal'),
        ('one_time', 'One-time event'),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    address_display = models.CharField(max_length=300, blank=True)
    address_full = models.CharField(max_length=500, blank=True)

    vendors = models.ManyToManyField(Farm, related_name='markets', blank=True)

    # Schedule
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, default='weekly')
    day_of_week = models.CharField(max_length=20, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    season_start = models.DateField(null=True, blank=True)
    season_end = models.DateField(null=True, blank=True)
    next_date = models.DateField(null=True, blank=True)

    contact_email = models.EmailField(blank=True)
    contact_website = models.URLField(blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['next_date', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def schedule_display(self):
        parts = []
        if self.day_of_week:
            parts.append(f"{self.get_frequency_display()} — {self.day_of_week}")
        if self.start_time and self.end_time:
            parts.append(f"{self.start_time.strftime('%-I:%M %p')} – {self.end_time.strftime('%-I:%M %p')}")
        if self.season_start and self.season_end:
            parts.append(f"{self.season_start.strftime('%b %d')} to {self.season_end.strftime('%b %d')}")
        return ' | '.join(parts) if parts else ''

    def vendor_count(self):
        return self.vendors.count()


class FarmPhoto(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='farm_photos/%Y/%m/')
    is_primary = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.farm.name} photo #{self.order}"

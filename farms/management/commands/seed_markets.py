from datetime import date, time
from django.core.management.base import BaseCommand
from farms.models import FarmersMarket


MARKETS = [
    {
        "name": "St. Albert Farmers' Market",
        "slug": "st-albert-farmers-market",
        "description": "Western Canada's largest outdoor farmers' market, running since 1983. Over 280 vendors offering produce, meat, dairy, baked goods, crafts, and more.",
        "address_display": "St. Albert, AB",
        "latitude": 53.6303,
        "longitude": -113.6271,
        "frequency": "weekly",
        "day_of_week": "Saturday",
        "start_time": time(10, 0),
        "end_time": time(15, 0),
        "season_start": date(2026, 6, 6),
        "season_end": date(2026, 10, 10),
        "next_date": date(2026, 6, 6),
        "contact_website": "https://stalbertfarmersmarket.com",
    },
    {
        "name": "Calgary Farmers' Market",
        "slug": "calgary-farmers-market",
        "description": "Year-round indoor market with 75+ vendors. Local meats, cheeses, produce, baked goods, and artisan products.",
        "address_display": "Calgary, AB",
        "latitude": 51.0100,
        "longitude": -114.0651,
        "frequency": "weekly",
        "day_of_week": "Thursday–Sunday",
        "start_time": time(9, 0),
        "end_time": time(17, 0),
        "season_start": None,
        "season_end": None,
        "next_date": date(2026, 3, 30),
        "contact_website": "https://calgaryfarmersmarket.ca",
    },
    {
        "name": "Old Strathcona Farmers' Market",
        "slug": "old-strathcona-farmers-market",
        "description": "Edmonton's beloved year-round market since 1983. Indoor market every Saturday with local produce, baked goods, meats, and crafts.",
        "address_display": "Edmonton, AB",
        "latitude": 53.5181,
        "longitude": -113.4958,
        "frequency": "weekly",
        "day_of_week": "Saturday",
        "start_time": time(8, 0),
        "end_time": time(15, 0),
        "season_start": None,
        "season_end": None,
        "next_date": date(2026, 3, 28),
        "contact_website": "https://osfm.ca",
    },
    {
        "name": "Millarville Farmers' Market",
        "slug": "millarville-farmers-market",
        "description": "Alberta's original country market, running since 1985 in the foothills south of Calgary. Over 200 vendors with local food, plants, and crafts.",
        "address_display": "Millarville, AB",
        "latitude": 50.7167,
        "longitude": -114.3333,
        "frequency": "weekly",
        "day_of_week": "Saturday",
        "start_time": time(9, 0),
        "end_time": time(14, 0),
        "season_start": date(2026, 6, 20),
        "season_end": date(2026, 9, 26),
        "next_date": date(2026, 6, 20),
        "contact_website": "https://millarvilleracetrack.com/farmers-market",
    },
    {
        "name": "Lethbridge Farmers' Market",
        "slug": "lethbridge-farmers-market",
        "description": "Southern Alberta's market hub with local produce, meats, baked goods, and artisan products. Indoor and outdoor spaces.",
        "address_display": "Lethbridge, AB",
        "latitude": 49.6942,
        "longitude": -112.8328,
        "frequency": "weekly",
        "day_of_week": "Wednesday & Saturday",
        "start_time": time(8, 0),
        "end_time": time(13, 0),
        "season_start": date(2026, 5, 1),
        "season_end": date(2026, 10, 31),
        "next_date": date(2026, 5, 2),
        "contact_website": "https://lethbridgefarmersmarket.ca",
    },
    {
        "name": "Red Deer Farmers' Market",
        "slug": "red-deer-farmers-market",
        "description": "Central Alberta's weekly market featuring local growers and producers. Fresh produce, honey, meats, preserves, and baked goods.",
        "address_display": "Red Deer, AB",
        "latitude": 52.2681,
        "longitude": -113.8112,
        "frequency": "weekly",
        "day_of_week": "Saturday",
        "start_time": time(9, 0),
        "end_time": time(13, 0),
        "season_start": date(2026, 5, 16),
        "season_end": date(2026, 10, 17),
        "next_date": date(2026, 5, 16),
        "contact_website": "https://reddeermarket.com",
    },
    {
        "name": "Bountiful Farmers' Market",
        "slug": "bountiful-farmers-market",
        "description": "Year-round indoor market in south Edmonton with over 200 vendors. Open Friday through Sunday with fresh local food, international cuisine, and artisan goods.",
        "address_display": "Edmonton, AB",
        "latitude": 53.4687,
        "longitude": -113.4552,
        "frequency": "weekly",
        "day_of_week": "Friday–Sunday",
        "start_time": time(9, 0),
        "end_time": time(17, 0),
        "season_start": None,
        "season_end": None,
        "next_date": date(2026, 3, 28),
        "contact_website": "https://bountifulmarket.com",
    },
]


class Command(BaseCommand):
    help = 'Seed Alberta farmers markets'

    def handle(self, *args, **options):
        created = 0
        for data in MARKETS:
            if FarmersMarket.objects.filter(slug=data['slug']).exists():
                continue
            FarmersMarket.objects.create(**data)
            created += 1

        self.stdout.write(self.style.SUCCESS(
            f'Created {created} markets ({FarmersMarket.objects.count()} total)'
        ))

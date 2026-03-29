from django.core.management.base import BaseCommand
from farms.models import Category


CATEGORIES = {
    ('Meat & Poultry', 'meat-poultry', '🥩'): [
        ('Beef', 'beef', '🐄'),
        ('Pork', 'pork', '🐖'),
        ('Chicken', 'chicken', '🐔'),
        ('Turkey', 'turkey', '🦃'),
        ('Lamb', 'lamb', '🐑'),
        ('Bison', 'bison', '🦬'),
        ('Game', 'game', '🦌'),
    ],
    ('Eggs', 'eggs', '🥚'): [
        ('Chicken Eggs', 'chicken-eggs', '🥚'),
        ('Duck Eggs', 'duck-eggs', '🦆'),
        ('Quail Eggs', 'quail-eggs', ''),
    ],
    ('Dairy', 'dairy', '🥛'): [
        ('Milk', 'milk', '🥛'),
        ('Cheese', 'cheese', '🧀'),
        ('Butter', 'butter', '🧈'),
        ('Yogurt', 'yogurt', ''),
        ('Cream', 'cream', ''),
    ],
    ('Produce', 'produce', '🥬'): [
        ('Vegetables', 'vegetables', '🥕'),
        ('Fruit', 'fruit', '🍎'),
        ('Herbs', 'herbs', '🌿'),
        ('Mushrooms', 'mushrooms', '🍄'),
        ('Microgreens', 'microgreens', '🌱'),
    ],
    ('Grains & Pulses', 'grains-pulses', '🌾'): [
        ('Wheat', 'wheat', '🌾'),
        ('Oats', 'oats', ''),
        ('Barley', 'barley', ''),
        ('Lentils', 'lentils', ''),
        ('Dried Beans', 'dried-beans', ''),
    ],
    ('Honey & Bee Products', 'honey-bee', '🍯'): [
        ('Honey', 'honey', '🍯'),
        ('Beeswax', 'beeswax', '🐝'),
        ('Pollen', 'pollen', ''),
    ],
    ('Preserves & Value-Add', 'preserves', '🫙'): [
        ('Jams & Jellies', 'jams-jellies', '🫙'),
        ('Pickles', 'pickles', '🥒'),
        ('Sauces', 'sauces', ''),
        ('Baked Goods', 'baked-goods', '🍞'),
        ('Dried Goods', 'dried-goods', ''),
    ],
    ('Plants & Nursery', 'plants-nursery', '🌻'): [
        ('Seedlings', 'seedlings', '🌱'),
        ('Perennials', 'perennials', '🌸'),
        ('Trees', 'trees', '🌳'),
        ('Seeds', 'seeds', ''),
    ],
    ('Fiber & Craft', 'fiber-craft', '🧶'): [
        ('Wool', 'wool', '🧶'),
        ('Alpaca Fiber', 'alpaca-fiber', '🦙'),
        ('Hides & Leather', 'hides-leather', ''),
    ],
    ('Experiences', 'experiences', '🚜'): [
        ('Farm Tours', 'farm-tours', '🚜'),
        ('U-Pick', 'u-pick', '🧺'),
        ('Farm Stays', 'farm-stays', '🏡'),
        ('Workshops', 'workshops', '📚'),
    ],
}


class Command(BaseCommand):
    help = 'Seed product categories and subcategories'

    def handle(self, *args, **options):
        created_count = 0
        for (parent_name, parent_slug, parent_icon), children in CATEGORIES.items():
            parent, created = Category.objects.get_or_create(
                slug=parent_slug,
                defaults={'name': parent_name, 'icon': parent_icon},
            )
            if created:
                created_count += 1

            for child_name, child_slug, child_icon in children:
                _, created = Category.objects.get_or_create(
                    slug=child_slug,
                    defaults={'name': child_name, 'icon': child_icon, 'parent': parent},
                )
                if created:
                    created_count += 1

        self.stdout.write(self.style.SUCCESS(f'Created {created_count} categories'))

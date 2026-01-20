from django.core.management.base import BaseCommand

from store.models import Product


class Command(BaseCommand):
    help = "Seed a few demo products for the simple store."

    def handle(self, *args, **options):
        demo_products = [
            {
                "name": "Classic T‑Shirt",
                "description": "Soft cotton tee. A simple classic.",
                "price": "19.99",
                "image_url": "https://images.unsplash.com/photo-1520975958225-1e23e43f962c?auto=format&fit=crop&w=1200&q=60",
            },
            {
                "name": "Running Shoes",
                "description": "Lightweight shoes for daily runs.",
                "price": "79.00",
                "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=1200&q=60",
            },
            {
                "name": "Coffee Mug",
                "description": "Ceramic mug for your morning coffee.",
                "price": "12.50",
                "image_url": "https://images.unsplash.com/photo-1517256064527-09c73fc73e38?auto=format&fit=crop&w=1200&q=60",
            },
            {
                "name": "Wireless Headphones",
                "description": "Comfortable over‑ear headphones.",
                "price": "129.99",
                "image_url": "https://images.unsplash.com/photo-1518441902117-f0a6a3f1ccf5?auto=format&fit=crop&w=1200&q=60",
            },
        ]

        created = 0
        for p in demo_products:
            obj, was_created = Product.objects.get_or_create(
                name=p["name"],
                defaults={
                    "description": p["description"],
                    "price": p["price"],
                    "image_url": p["image_url"],
                    "is_active": True,
                },
            )
            if was_created:
                created += 1
            else:
                obj.description = p["description"]
                obj.price = p["price"]
                obj.image_url = p["image_url"]
                obj.is_active = True
                obj.save()

        self.stdout.write(self.style.SUCCESS(f"Seeded products. Created: {created}, Updated: {len(demo_products) - created}"))


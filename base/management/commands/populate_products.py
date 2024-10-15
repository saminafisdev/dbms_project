from django.core.management.base import BaseCommand
from base.models import Product, Category  # Adjust the import to your app name


class Command(BaseCommand):
    help = "Populate the database with random products and categories"

    def handle(self, *args, **kwargs):
        categories = [
            Category.objects.create(
                name="Electronics", description="Various electronic items."
            ),
            Category.objects.create(
                name="Accessories", description="Different accessories."
            ),
            Category.objects.create(
                name="Computers", description="Computer related items."
            ),
        ]

        # Create sample products
        products = [
            {
                "name": "Wireless Mouse",
                "description": "Ergonomic wireless mouse with 2.4GHz connection.",
                "unit_price": 25.99,
                "stock": 150,
                "category": categories[0],  # Electronics
            },
            {
                "name": "Gaming Keyboard",
                "description": "RGB mechanical gaming keyboard with customizable keys.",
                "unit_price": 69.99,
                "stock": 75,
                "category": categories[0],  # Electronics
            },
            {
                "name": "Bluetooth Headphones",
                "description": "Noise-cancelling Bluetooth headphones for music and calls.",
                "unit_price": 89.99,
                "stock": 100,
                "category": categories[0],  # Electronics
            },
            {
                "name": "USB-C Hub",
                "description": "Multi-port USB-C hub with HDMI, USB 3.0, and SD card reader.",
                "unit_price": 39.99,
                "stock": 200,
                "category": categories[1],  # Accessories
            },
            {
                "name": "External SSD",
                "description": "Portable external SSD with 1TB storage.",
                "unit_price": 129.99,
                "stock": 50,
                "category": categories[1],  # Accessories
            },
            {
                "name": "Fitness Tracker",
                "description": "Water-resistant fitness tracker with heart rate monitor.",
                "unit_price": 59.99,
                "stock": 120,
                "category": categories[1],  # Accessories
            },
            {
                "name": "Laptop Backpack",
                "description": "Durable backpack with multiple compartments for laptops and accessories.",
                "unit_price": 49.99,
                "stock": 80,
                "category": categories[2],  # Computers
            },
        ]

        for product_data in products:
            product = Product(**product_data)
            product.save()

        self.stdout.write(
            self.style.SUCCESS("Successfully populated products and categories.")
        )

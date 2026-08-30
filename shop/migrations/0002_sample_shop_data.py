from decimal import Decimal

from django.db import migrations


def create_sample_data(apps, schema_editor):
    Category = apps.get_model("shop", "Category")
    Product = apps.get_model("shop", "Product")

    laptops = Category.objects.create(
        name="Laptops",
        slug="laptops",
        description="Portable computers for study, work, and gaming.",
    )
    phones = Category.objects.create(
        name="Phones",
        slug="phones",
        description="Smartphones for everyday communication and entertainment.",
    )
    accessories = Category.objects.create(
        name="Accessories",
        slug="accessories",
        description="Useful devices and accessories for your setup.",
    )

    Product.objects.bulk_create(
        [
            Product(
                category=laptops,
                name="Lenovo IdeaPad 5",
                slug="lenovo-ideapad-5",
                description="Balanced laptop with a bright display and fast SSD.",
                price=Decimal("28999.00"),
                stock=8,
                image_url="https://images.unsplash.com/photo-1496181133206-80ce9b88a853",
            ),
            Product(
                category=laptops,
                name="ASUS TUF Gaming",
                slug="asus-tuf-gaming",
                description="Gaming laptop with dedicated graphics and strong cooling.",
                price=Decimal("42999.00"),
                stock=4,
                image_url="https://images.unsplash.com/photo-1603302576837-37561b2e2302",
            ),
            Product(
                category=phones,
                name="Samsung Galaxy A55",
                slug="samsung-galaxy-a55",
                description="Modern smartphone with AMOLED display and great battery life.",
                price=Decimal("17999.00"),
                stock=12,
                image_url="https://images.unsplash.com/photo-1511707171634-5f897ff02aa9",
            ),
            Product(
                category=phones,
                name="iPhone 15",
                slug="iphone-15",
                description="Fast smartphone with a powerful camera system.",
                price=Decimal("37999.00"),
                stock=5,
                image_url="https://images.unsplash.com/photo-1592750475338-74b7b21085ab",
            ),
            Product(
                category=accessories,
                name="Logitech Wireless Mouse",
                slug="logitech-wireless-mouse",
                description="Comfortable wireless mouse for work and study.",
                price=Decimal("1299.00"),
                stock=25,
                image_url="https://images.unsplash.com/photo-1527814050087-3793815479db",
            ),
            Product(
                category=accessories,
                name="USB-C Hub",
                slug="usb-c-hub",
                description="Compact hub with HDMI, USB, and card reader ports.",
                price=Decimal("2199.00"),
                stock=15,
                image_url="https://images.unsplash.com/photo-1625842268584-8f3296236761",
            ),
        ]
    )


def remove_sample_data(apps, schema_editor):
    Category = apps.get_model("shop", "Category")
    Category.objects.filter(slug__in=["laptops", "phones", "accessories"]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_sample_data, remove_sample_data),
    ]

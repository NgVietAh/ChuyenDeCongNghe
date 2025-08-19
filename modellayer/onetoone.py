import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from myapp.models import Place, Restaurant

def create_and_show_restaurant():
 
    place, created = Place.objects.get_or_create(
        name="Pizza Palace",
        defaults={
            "address": "123 Main St",
            "phone_number": "555-1234"
        }
    )

    restaurant, created = Restaurant.objects.get_or_create(
        place=place,
        defaults={
            "serves_hot_dogs": True,
            "serves_pizza": True
        }
    )

    print("Địa chỉ nhà hàng:", restaurant.place.address)
    print("Phục vụ pizza:", place.restaurant.serves_pizza)

if __name__ == "__main__":
    create_and_show_restaurant()

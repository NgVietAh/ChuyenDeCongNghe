import os
import django

# Khởi động Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from myapp.models import Pizza, Topping

# Xoá dữ liệu cũ cho dễ test
Pizza.objects.all().delete()
Topping.objects.all().delete()

# Tạo topping
cheese = Topping.objects.create(name="Cheese")
pepperoni = Topping.objects.create(name="Pepperoni")
mushroom = Topping.objects.create(name="Mushroom")

# Tạo pizza
margherita = Pizza.objects.create(name="Margherita")
pepperoni_pizza = Pizza.objects.create(name="Pepperoni Pizza")

# Gắn topping cho pizza
margherita.toppings.add(cheese, mushroom)
pepperoni_pizza.toppings.add(cheese, pepperoni)

# --- Truy vấn ---
print("Margherita toppings:", margherita.toppings.all())  

print("Pepperoni Pizza toppings:", pepperoni_pizza.toppings.all())  

print("Cheese có trong các pizza:", cheese.pizza_set.all())  
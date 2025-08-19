import os
import django

# Thiết lập Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from myapp.models import Place, Supplier

# Xóa dữ liệu cũ để test
Place.objects.all().delete()
Supplier.objects.all().delete()

# Tạo các Place
p1 = Place.objects.create(name="Cafe A")
p2 = Place.objects.create(name="Cafe B")
p3 = Place.objects.create(name="Cafe C")

# Tạo Supplier
s1 = Supplier.objects.create(name="Supplier X")
s2 = Supplier.objects.create(name="Supplier Y")

# Gán khách hàng cho Supplier
s1.customers.add(p1, p2)
s2.customers.add(p2, p3)

# In dữ liệu ra terminal
print("Customers of Supplier X:", list(s1.customers.all()))
print("Customers of Supplier Y:", list(s2.customers.all()))
print("Suppliers of Cafe B:", list(p2.providers.all()))
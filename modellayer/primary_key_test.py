import os
import django

# Thiết lập môi trường Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from myapp.models import Fruit

fruit = Fruit.objects.create(name="Apple")

# Thay đổi name -> "Pear" (do name là primary_key, Django sẽ tạo thêm object mới)
fruit.name = "Pear"
fruit.save()

# Xem danh sách tất cả fruits trong database
print(list(Fruit.objects.values_list("name", flat=True)))

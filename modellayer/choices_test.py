import os
import django

# Thiết lập môi trường Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from myapp.models import Person

# Tạo object Person
p = Person(first_name="Fred", shirt_size="L")
p.save()

# In ra giá trị lưu trong DB
print("Giá trị trong DB:", p.shirt_size)

# In ra giá trị display theo choices
print("Giá trị hiển thị:", p.get_shirt_size_display())

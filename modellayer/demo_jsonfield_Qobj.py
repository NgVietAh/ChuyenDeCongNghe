import os
import django
from django.db.models import Q

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from myapp.models import Dog

# Xóa dữ liệu cũ
Dog.objects.all().delete()

# Tạo dữ liệu demo
Dog.objects.create(name="Rufus", data={"breed": "labrador", "owner": "Bob"})
Dog.objects.create(name="Meg", data={"breed": "collie", "owner": "Bob"})
Dog.objects.create(name="Fred", data={})
Dog.objects.create(name="Merry", data={"breed": "pekingese", "tricks": ["fetch", "dance"]})
Dog.objects.create(name="Max", data=None)
Dog.objects.create(name="Archie", data=None)

# Truy vấn JSONField với Q objects
dogs_q = Dog.objects.filter(Q(data__owner="Bob") | Q(data__breed="pekingese"))
print("Dogs with owner='Bob' OR breed='pekingese':", list(dogs_q))

dogs_no_owner = Dog.objects.filter(~Q(data__has_key="owner"))
print("Dogs without owner:", list(dogs_no_owner))

dogs_null_or_empty = Dog.objects.filter(Q(data__isnull=True) | Q(data__exact={}))
print("Dogs with data null or empty:", list(dogs_null_or_empty))

# Sao chép một instance
rufus = Dog.objects.get(name="Rufus")
rufus.pk = None
rufus.save()
print("Copied Rufus:", rufus)

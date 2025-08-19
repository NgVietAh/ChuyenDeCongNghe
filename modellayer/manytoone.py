import os
import django

# Cấu hình Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from myapp.models import Manufacturer, Car

toyota = Manufacturer.objects.create(name="Toyota")
bmw = Manufacturer.objects.create(name="BMW")

#xe thuộc toyota
car1 = Car.objects.create(name="Corolla", manufacturer=toyota)
car2 = Car.objects.create(name="Camry", manufacturer=toyota)

#xe thuộc bmw
car3 = Car.objects.create(name="X5", manufacturer=bmw)

#truy vấn từ xe -> hãng
print(car1.manufacturer.name)

#ngược lại
print(toyota.car_set.all())     
print(bmw.car_set.all())        
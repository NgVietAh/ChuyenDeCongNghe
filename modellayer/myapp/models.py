from django.db import models

class Musician(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    instrument = models.CharField(max_length=100)

class Album(models.Model):
    artist = models.ForeignKey(Musician, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    release_date = models.DateField()
    num_stars = models.IntegerField()

class Person(models.Model):
    SHIRT_SIZES = [
        ("S", "Small"),
        ("M", "Medium"),
        ("L", "Large"),
    ]

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    shirt_size = models.CharField(max_length=1, choices=SHIRT_SIZES, default="M")

class Runner(models.Model):
    class MedalType(models.TextChoices):
        GOLD = "GOLD", "Gold Medal"
        SILVER = "SILVER", "Silver Medal"
        BRONZE = "BRONZE", "Bronze Medal"

    name = models.CharField(max_length=60)
    medal = models.CharField(max_length=10, choices=MedalType, blank=True)

class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(
        help_text="Please enter your school email address",
        unique=True
    )

class Fruit(models.Model):
    name = models.CharField(max_length=100, primary_key=True)

# Model Hãng sản xuất
class Manufacturer(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Model Xe hơi
class Car(models.Model):
    name = models.CharField(max_length=100)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.manufacturer.name}"

class Topping(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Pizza(models.Model):
    name = models.CharField(max_length=100)
    toppings = models.ManyToManyField(Topping)

    def __str__(self):
        return self.name
from django.db import models
from django.utils.text import slugify

# Create your models here.

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

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

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

class Group(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(Person, through="Membership")

    def __str__(self):
        return self.name


class Membership(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date_joined = models.DateField()
    invite_reason = models.CharField(max_length=64)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["person", "group"], name="unique_person_group"
            )
        ]

class Place(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    
class Supplier(Place):
    customers = models.ManyToManyField(Place, related_name='providers')

    def __str__(self):
        return f"Supplier: {self.name}"

class Restaurant(models.Model):
    place = models.OneToOneField(
        Place,
        on_delete=models.CASCADE,  
        primary_key=True      
    )
    serves_hot_dogs = models.BooleanField(default=False)
    serves_pizza = models.BooleanField(default=False)

    def __str__(self):
        return f"Restaurant: {self.place.name}"
    
class Blog(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True)

    def save(self, **kwargs):
        self.slug = slugify(self.name)
        if (update_fields := kwargs.get("update_fields")) is not None and "name" in update_fields:
            kwargs["update_fields"] = {"slug"}.union(update_fields)
        super().save(**kwargs)

#abstract
#Kế thừa meta từ nhiều class
class CommonInfo(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()

    class Meta:
        abstract = True
        ordering = ["name"]

class Unmanaged(models.Model):
    class Meta:
        abstract = True
        managed = False

class Student(CommonInfo, Unmanaged):
    home_group = models.CharField(max_length=5)

    class Meta(CommonInfo.Meta, Unmanaged.Meta):
        pass
# Khi dùng ForeignKey hoặc ManyToManyField trong abstract base class, phải đảm bảo unique reverse name và query name.
# Nếu dùng cùng related_name cho nhiều child class, sẽ gây lỗi khi migrate hoặc chạy system check.
# Giải quyết = cách dùng placeholder %()
# class Base(models.Model):
#     m2m = models.ManyToManyField(
#         OtherModel,
#         related_name="%(app_label)s_%(class)s_related",
#         related_query_name="%(app_label)s_%(class)ss",
#     )

#     class Meta:
#         abstract = True

# class ChildA(Base):
#     pass

# class ChildB(Base):
#     pass

# Kế thừa nhiều lớp
# class Article(models.Model):
#     article_id = models.AutoField(primary_key=True)
#     title = models.CharField(max_length=50)

# class Book(models.Model):
#     book_id = models.AutoField(primary_key=True)
#     title = models.CharField(max_length=50)

# class BookReview(Book, Article):
#     review_text = models.TextField()

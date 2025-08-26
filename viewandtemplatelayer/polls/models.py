from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Poll(models.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField(default=timezone.now) 

    def __str__(self):
        return self.question

class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)

    def __str__(self):
        return self.choice_text

from django.urls import reverse

class Author(models.Model):
    name = models.CharField(max_length=200)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse("author-detail", kwargs={"pk": self.pk})
from django.db import models

class Publisher(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

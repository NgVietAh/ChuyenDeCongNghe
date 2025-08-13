import os
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from polls.models import Question

q = Question(question_text="What's new?", pub_date=timezone.now())
q.save()

print(f"Created question with ID: {q.id}")

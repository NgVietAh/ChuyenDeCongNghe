import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from polls.models import Question, Choice
from django.utils import timezone

def run():
    print(Question.objects.all())

    q = Question.objects.filter(id=1).first()
    print(q)

    current_year = timezone.now().year

    questions = Question.objects.filter(pub_date__year=current_year)
    if questions.exists():
        for question in questions:
            print(question)
    else:
        print("Không có câu hỏi nào xuất bản năm nay.")

    if q:
        print(q.was_published_recently())

        q.choice_set.create(choice_text="Not much", votes=0)
        q.choice_set.create(choice_text="The sky", votes=0)
        c = q.choice_set.create(choice_text="Just hacking again", votes=0)
        print(c.question)

        print(q.choice_set.all())
        print(q.choice_set.count())

        c_to_delete = q.choice_set.filter(choice_text__startswith="Just hacking")
        c_to_delete.delete()
        print("Deleted choices:", c_to_delete)

if __name__ == '__main__':
    run()

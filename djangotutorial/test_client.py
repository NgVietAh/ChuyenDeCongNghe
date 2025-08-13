import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.test import Client
from django.urls import reverse, NoReverseMatch

def run_client_tests():
    client = Client()

    # Test '/'
    response = client.get("/")
    print(f"GET / -> status: {response.status_code}")

    # Test '/polls/'
    try:
        url = reverse("polls:index")
    except NoReverseMatch as e:
        print("Error in reverse():", e)
        return

    response = client.get(url)
    print(f"GET {url} -> status: {response.status_code}")

    if response.status_code == 200 and response.context:
        latest_questions = response.context.get("latest_question_list", None)
        print("Latest question list:", latest_questions)
    else:
        print("No context data or non-200 response.")

if __name__ == '__main__':
    run_client_tests()

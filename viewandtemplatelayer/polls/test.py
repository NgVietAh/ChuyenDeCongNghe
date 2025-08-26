from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from .models import Poll
from .views import my_custom_404_view

client = Client()

# Test Poll detail view
class PollDetailViewTests(TestCase):
    def setUp(self):
        self.poll = Poll.objects.create(question="Bài kiểm tra đầu tiên")

    def test_detail_view_status_code(self):
        url = reverse('polls:detail', kwargs={'poll_id': self.poll.id})
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Bài kiểm tra đầu tiên")

    def test_detail_view_404(self):
        url = reverse('polls:detail', kwargs={'poll_id': 999})
        response = client.get(url)
        self.assertEqual(response.status_code, 404)

# Test custom 404
@override_settings(ROOT_URLCONF=__name__)
class Custom404Tests(TestCase):
    def test_custom_404_view(self):
        response = client.get("/nonexistent-url/")
        self.assertEqual(response.status_code, 404)

# Test custom 403
def response_error_handler(request, exception=None):
    return HttpResponse("Error handler content", status=403)

def permission_denied_view(request):
    raise PermissionDenied

@override_settings(ROOT_URLCONF=__name__)
class Custom403Tests(TestCase):
    def test_custom_403_view(self):
        url = "/403/"
        # tạo URL tạm để test view permission_denied_view
        response = client.get(url)
        self.assertEqual(response.status_code, 403)

# Test custom 500

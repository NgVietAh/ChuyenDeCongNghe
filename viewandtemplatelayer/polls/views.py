from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.views import View
from polls.forms import ContactForm
from django.contrib.auth.mixins import LoginRequiredMixin
from polls.models import Author
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView, ListView, FormView, CreateView, DeleteView, UpdateView
from .models import Poll
import datetime

class PollDetailView(DetailView):
    model = Poll
    template_name = "polls/detail.html"
    context_object_name = "poll"
    pk_url_kwarg = "poll_id"  # match URL /poll/<int:poll_id>/


class PollListView(ListView):
    model = Poll
    template_name = "polls/index.html"
    context_object_name = "poll_list"

class CurrentDateTimeView(View):
    async def get(self, request):
        now = datetime.datetime.now()
        html = '<html lang="en"><body>It is now %s.</body></html>' % now
        return HttpResponse(html)

class Special2003View(TemplateView):
    template_name = "polls/special_2003.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = "Đây là bài viết đặc biệt năm 2003"
        return context

class YearArchiveView(View):
    def get(self, request, year):
        return HttpResponse(f"Các bài viết năm {year}")

class MonthArchiveView(View):
    def get(self, request, year, month):
        return HttpResponse(f"Các bài viết tháng {month}/{year}")

class ArticleDetailView(View):
    def get(self, request, year, month, slug):
        return HttpResponse(f"Chi tiết bài viết {slug} - {month}/{year}")

class GoTo2025View(View):
    def get(self, request):
        url = reverse('polls:year-archive', kwargs={'year': 2025})
        return HttpResponseRedirect(url)

def my_custom_404_view(request, exception):
    return render(request, "polls/404.html", status=404)

class ContactFormView(FormView):
    template_name = "contact.html"
    form_class = ContactForm
    success_url = "/thanks/"

    def form_valid(self, form):
        # Gọi phương thức send_email() sau khi form hợp lệ
        form.send_email()
        return super().form_valid(form)
    
class AuthorCreateView(LoginRequiredMixin, CreateView):
    model = Author
    fields = ["name"]

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class AuthorUpdateView(UpdateView):
    model = Author
    fields = ["name"]


class AuthorDeleteView(DeleteView):
    model = Author
    success_url = reverse_lazy("author-list")

from django.http import JsonResponse

class JsonableResponseMixin:
    """
    Mixin to add JSON support to a form.
    Must be used with an object-based FormView (e.g. CreateView).
    """

    accepted_media_types = ["text/html", "application/json"]

    def dispatch(self, request, *args, **kwargs):
        if request.get_preferred_type(self.accepted_media_types) is None:
            # No format in common.
            return HttpResponse(
                status_code=406, headers={"Accept": ",".join(self.accepted_media_types)}
            )

        return super().dispatch(request, *args, **kwargs)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        accepted_type = self.request.get_preferred_type(self.accepted_media_types)
        if accepted_type == "text/html":
            return response
        elif accepted_type == "application/json":
            return JsonResponse(form.errors, status=400)

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super().form_valid(form)
        accepted_type = self.request.get_preferred_type(self.accepted_media_types)
        if accepted_type == "text/html":
            return response
        elif accepted_type == "application/json":
            data = {
                "pk": self.object.pk,
            }
            return JsonResponse(data)

from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.views.generic.detail import SingleObjectMixin
from polls.models import Author, Publisher

class RecordInterestView(SingleObjectMixin, View):
    """Records the current user's interest in an author."""

    model = Author

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()

        # Look up the author we're interested in.
        self.object = self.get_object()
        # Actually record interest somehow here!

        return HttpResponseRedirect(
            reverse("author-detail", kwargs={"pk": self.object.pk})
        )
    
class PublisherDetailView(SingleObjectMixin, ListView):
    paginate_by = 2
    template_name = "polls/publisher_detail.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Publisher.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["publisher"] = self.object
        return context

    def get_queryset(self):
        return self.object.book_set.all()
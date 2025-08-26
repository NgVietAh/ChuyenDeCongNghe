# from django.http import HttpResponse

# def special_case_2003(request):
#     return HttpResponse("Đây là bài viết đặc biệt năm 2003")

# def year_archive(request, year):
#     return HttpResponse(f"Các bài viết năm {year}")

# def month_archive(request, year, month):
#     return HttpResponse(f"Các bài viết tháng {month}/{year}")

# def article_detail(request, year, month, slug):
#     return HttpResponse(f"Chi tiết bài viết {slug} - {month}/{year}")

from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
import datetime
from .models import Poll

async def current_datetime(request):
    now = datetime.datetime.now()
    html = '<html lang="en"><body>It is now %s.</body></html>' % now
    return HttpResponse(html)

def index(request):
    return render(request, 'polls/index.html')

def special_case_2003(request):
    return HttpResponse("Đây là bài viết đặc biệt năm 2003")

def year_archive(request, year):
    return HttpResponse(f"Các bài viết năm {year}")

def month_archive(request, year, month):
    return HttpResponse(f"Các bài viết tháng {month}/{year}")

def article_detail(request, year, month, slug):
    return HttpResponse(f"Chi tiết bài viết {slug} - {month}/{year}")

def go_to_2025(request):
    url = reverse('polls:year-archive', kwargs={'year': 2025})
    return HttpResponseRedirect(url)

def detail(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    return render(request, "polls/detail.html", {"poll": poll})

def my_custom_404_view(request, exception):
    return render(request, "polls/404.html", status=404)
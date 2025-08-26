# from django.http import HttpResponse

# def special_case_2003(request):
#     return HttpResponse("Đây là bài viết đặc biệt năm 2003")

# def year_archive(request, year):
#     return HttpResponse(f"Các bài viết năm {year}")

# def month_archive(request, year, month):
#     return HttpResponse(f"Các bài viết tháng {month}/{year}")

# def article_detail(request, year, month, slug):
#     return HttpResponse(f"Chi tiết bài viết {slug} - {month}/{year}")

from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django.http import HttpResponseRedirect

def index(request):
    # Render template với link dùng {% url %}
    return render(request, 'polls/index.html')

def special_case_2003(request):
    return HttpResponse("Đây là bài viết đặc biệt năm 2003")

def year_archive(request, year):
    return HttpResponse(f"Các bài viết năm {year}")

def month_archive(request, year, month):
    return HttpResponse(f"Các bài viết tháng {month}/{year}")

def article_detail(request, year, month, slug):
    return HttpResponse(f"Chi tiết bài viết {slug} - {month}/{year}")

# Ví dụ reverse URL trong views
def go_to_2025(request):
    url = reverse('polls:year-archive', kwargs={'year': 2025})
    return HttpResponseRedirect(url)

# from django.urls import path, re_path, include
# from . import views

# app_name = "polls"

# article_patterns = [
#     path("2003/", views.special_case_2003, name="special-case-2003"),
#     re_path(r"^(?P<year>[0-9]{4})/$", views.year_archive, name="year-archive"),
#     re_path(r"^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$", views.month_archive, name="month-archive"),
#     re_path(
#         r"^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<slug>[\w-]+)/$",
#         views.article_detail,
#         name="article-detail",
#     ),
# ]

# urlpatterns = [
#     path("articles/", include(article_patterns)),
# ]

#Dùng template
from django.urls import path, re_path, include
from . import views

app_name = "polls"

article_patterns = [
    path("", views.index, name="index"),
    path("2003/", views.special_case_2003, name="special-case-2003"),
    re_path(r"^(?P<year>[0-9]{4})/$", views.year_archive, name="year-archive"),
    re_path(r"^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$", views.month_archive, name="month-archive"),
    re_path(r"^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<slug>[\w-]+)/$", views.article_detail, name="article-detail"),
]

urlpatterns = [
    path("articles/", include(article_patterns)),
    path('time/', views.current_datetime, name='current-datetime'),
    path("poll/<int:poll_id>/", views.detail, name="detail"),
    path("go-to-2025/", views.go_to_2025, name="go-to-2025"),
]
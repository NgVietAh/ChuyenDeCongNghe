from django.urls import path, re_path, include
from .views import (
    PollDetailView,
    PollListView,
    CurrentDateTimeView,
    Special2003View,
    YearArchiveView,
    MonthArchiveView,
    ArticleDetailView,
    GoTo2025View,
    AuthorCreateView, AuthorDeleteView, AuthorUpdateView, RecordInterestView
)

app_name = "polls"

article_patterns = [
    path("", PollListView.as_view(), name="index"),
    path("2003/", Special2003View.as_view(), name="special-case-2003"),
    re_path(r"^(?P<year>[0-9]{4})/$", YearArchiveView.as_view(), name="year-archive"),
    re_path(r"^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$", MonthArchiveView.as_view(), name="month-archive"),
    re_path(r"^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<slug>[\w-]+)/$", ArticleDetailView.as_view(), name="article-detail"),
]

urlpatterns = [
    path("articles/", include(article_patterns)),
    path("time/", CurrentDateTimeView.as_view(), name="current-datetime"),
    path("poll/<int:poll_id>/", PollDetailView.as_view(), name="detail"),
    path("go-to-2025/", GoTo2025View.as_view(), name="go-to-2025"),
    path("author/add/", AuthorCreateView.as_view(), name="author-add"),
    path("author/<int:pk>/", AuthorUpdateView.as_view(), name="author-update"),
    path("author/<int:pk>/delete/", AuthorDeleteView.as_view(), name="author-delete"),
    path(
        "author/<int:pk>/interest/",
        RecordInterestView.as_view(),
        name="author-interest",
    ),

]

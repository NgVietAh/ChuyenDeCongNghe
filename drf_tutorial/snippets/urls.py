from django.urls import path, include
from rest_framework.routers import DefaultRouter
from snippets import views

# Tạo router và đăng ký các ViewSet
router = DefaultRouter()
router.register(r'snippets', views.SnippetViewSet, basename='snippet')
router.register(r'users', views.UserViewSet, basename='user')

# Tự động tạo URL từ ViewSet
urlpatterns = [
    path('', include(router.urls)),
]

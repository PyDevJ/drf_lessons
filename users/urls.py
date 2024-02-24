from django.urls import path
from users import views, apps

from rest_framework import routers

app_name = apps.UsersConfig.name

router = routers.DefaultRouter()
router.register(r'profile', views.UserViewSet, basename='profile')

urlpatterns = [
    path('payment/', views.PaymentListView.as_view(), name='payment'),
] + router.urls

from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users import views, apps

from rest_framework import routers

app_name = apps.UsersConfig.name

router = routers.DefaultRouter()
router.register(r'profile', views.UserViewSet, basename='profile')
router.register(r'payment', views.PaymentViewSet, basename='payment')

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.UserRegistrationView.as_view(), name='user_registration'),
    path('payment/create/', views.PaymentCreateAPIView.as_view(), name='payment_create'),
] + router.urls

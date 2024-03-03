from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from users.models import Payment, User
from users.serializers import PaymentSerializer, UserSerializer, UserRegistrationSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # Доступ только аутентифицированным пользователям
    permission_classes = [IsAuthenticated]


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    # Доступ всем пользователям
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        return Response({'message': 'User registered successfully', 'user_data': serializer.data})

    def perform_create(self, serializer):
        user = serializer.save()
        # Вывод информации о регистрации пользователя в консоль
        print(f"New user registered: {user.email}, {user.phone}, {user.city}, {user.avatar}")
        return user


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = (OrderingFilter, DjangoFilterBackend)
    ordering_fields = ('date_of_payment',)
    filterset_fields = ('payed_course', 'payed_lesson', 'payment_type')
    permission_classes = [IsAuthenticated]

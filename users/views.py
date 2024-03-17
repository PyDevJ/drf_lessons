from django.utils import timezone
from rest_framework import viewsets, generics, status
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import Payment, User
from users.serializers import PaymentSerializer, UserSerializer, UserRegistrationSerializer
from users.services import create_product, create_price


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


class PaymentCreateAPIView(APIView):
    """Создание платежа"""
    def post(self, request, format=None):
        # Получает пользователя
        payer = request.user
        # Получает сумму оплаты из запроса
        amount = request.data.get('amount')
        # Получает данные о способе оплаты ('bank' перевод на счет)
        payment_type = 'bank'
        # payment_type = request.data.get('payment_type')

        # Создание продукта в Stripe
        product_id = create_product("Course Subscription", "Subscription to course")
        # Создание цены в Stripe
        price_id = create_price(product_id, amount, 'RUB')

        # Установка текущей даты и времени для платежа, поле date_of_payment
        date_of_payment = timezone.now()

        # Создание записи о платеже в базе данных
        payment = Payment.objects.create(payer=payer, amount=amount, payment_type=payment_type,
                                         product_id=product_id, price_id=price_id, date_of_payment=date_of_payment)

        # Создание сессии для платежа в Stripe
        success_url = "http://example.com/success"  # URL для перехода при успешном платеже
        cancel_url = "http://127.0.0.1:8000/users/register/"  # URL для перехода при отмене платежа
        session_url = payment.create_checkout_session(success_url, cancel_url)

        if session_url:
            # Если сессия создана успешно, возвращает URL для оплаты
            return Response({'session_url': session_url}, status=status.HTTP_201_CREATED)
        else:
            # Если возникла ошибка при создании сессии, возвращает соответствующий ответ
            return Response({'error': 'Failed to create checkout session'}, status=status.HTTP_400_BAD_REQUEST)

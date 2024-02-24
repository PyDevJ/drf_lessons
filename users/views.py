from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from users.models import Payment, User
from users.serializers import PaymentSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PaymentListView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = (OrderingFilter, DjangoFilterBackend)
    ordering_fields = ('date_of_payment',)
    filterset_fields = ('payed_course', 'payed_lesson', 'payment_type')

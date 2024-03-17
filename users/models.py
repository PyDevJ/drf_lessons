from django.contrib.auth.models import AbstractUser
from django.db import models

from lms.models import Course, Lesson
from users.services import create_checkout_session

NULLABLE = {'null': True, 'blank': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='email')
    phone = models.CharField(max_length=20, verbose_name='телефон', **NULLABLE)
    city = models.CharField(max_length=50, verbose_name='город', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватарка', **NULLABLE)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


class Payment(models.Model):
    class PaymentType(models.TextChoices):
        CASH = 'cash', 'Наличными'
        BANK = 'bank', 'Перевод на счёт'

    payer = models.ForeignKey(User, on_delete=models.SET_NULL, **NULLABLE, verbose_name='плательщик', related_name='payer')
    date_of_payment = models.DateField(auto_now=True, verbose_name='дата оплаты')
    payed_course = models.ForeignKey(Course, on_delete=models.SET_NULL, **NULLABLE, verbose_name='оплаченный курс')
    payed_lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, **NULLABLE, verbose_name='оплаченный урок')
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='сумма оплаты')
    payment_type = models.CharField(max_length=20, choices=PaymentType.choices, verbose_name='способ оплаты')
    product_id = models.CharField(max_length=50, **NULLABLE)
    price_id = models.CharField(max_length=50, **NULLABLE)

    def create_checkout_session(self, success_url, cancel_url):
        """Создание сессии для платежа."""
        if not self.product_id or not self.price_id:
            return None
        return create_checkout_session(self.price_id, success_url, cancel_url)

    def __str__(self):
        return f'{self.payer} - {self.payed_course if self.payed_course else self.payed_lesson} - {self.amount}'

    class Meta:
        verbose_name = 'оплата'
        verbose_name_plural = 'оплаты'
        ordering = ('payer', 'date_of_payment')

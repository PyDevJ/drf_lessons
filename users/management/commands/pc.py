from django.core.management import BaseCommand
import datetime

from lms.models import Course, Lesson
from users.models import User, Payment


class Command(BaseCommand):
    help = 'Create sample payment objects'

    def handle(self, *args, **kwargs):
        # Создание: курсы
        course1 = Course.objects.create(name='курс первый')
        course2 = Course.objects.create(name='курс второй')

        # Создание: уроки
        lesson1 = Lesson.objects.create(name='урок первый')
        lesson2 = Lesson.objects.create(name='урок второй')
        lesson3 = Lesson.objects.create(name='урок третий из второго курса', course=course2)
        lesson4 = Lesson.objects.create(name='урок четвёртый из второго курса', course=course2)

        # Создание: пользователи
        user1, created = User.objects.get_or_create(email='user1@test.com')
        user2, created = User.objects.get_or_create(email='user2@test.com')

        # Создание: платежи
        payment1 = Payment.objects.create(
            payer=user1,
            date_of_payment=datetime.datetime.now().date(),
            amount=1000,
            payment_type='cash',
            payed_course=course1,
            payed_lesson=lesson1,
        )

        payment2 = Payment.objects.create(
            payer=user2,
            date_of_payment=datetime.datetime.now().date(),
            amount=2000,
            payment_type='cash',
            payed_course=course2,
            payed_lesson=lesson3,
        )

        self.stdout.write(self.style.SUCCESS('Successfully created payment objects'))

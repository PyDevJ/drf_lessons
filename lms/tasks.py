from datetime import timedelta
from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils import timezone
from lms.models import Course, CourseSubscription


@shared_task
def send_course_update_email(course_id):
    course = Course.objects.get(id=course_id)

    # Проверяется, прошло ли более 4 часов с момента последнего обновления
    if timezone.now() - course.updated_at > timedelta(hours=4):

        # Отправляется уведомление на электронную почту
        send_mail(
            'Course Update Notification',
            'The course you subscribed to has been updated.',
            'from@example.com',
            [CourseSubscription.user.email],
            fail_silently=False,
        )

        # Обновляется время последнего уведомления
        course.updated_at = timezone.now()
        course.save()


@shared_task
def block_inactive_users():
    # Создаётся модель пользователя
    user = get_user_model()

    # Определяется период неактивности пользователя (30 дней)
    inactive_period = timezone.now() - timezone.timedelta(days=30)

    # Создаётся список пользователей, которые не заходили в систему 30 дней
    inactive_users = user.objects.filter(last_login__lte=inactive_period)

    # Блокировка пользователей из списка неактивных 30 дней
    inactive_users.update(is_active=False)

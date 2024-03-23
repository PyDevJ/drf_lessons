from datetime import timedelta
from celery import shared_task
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

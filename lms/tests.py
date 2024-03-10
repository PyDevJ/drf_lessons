from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from lms.models import Lesson, Course, CourseSubscription

User = get_user_model()


class CourseLessonSubscriptionAPITest(TestCase):
    def setUp(self):
        """
        Устанавливаются начальные данные для тестов.
        """
        # Создание клиента API
        self.client = APIClient()

        # Удаление всех уроков перед созданием новых
        Lesson.objects.all().delete()

        # Создание пользователей
        self.user_moderator = User.objects.create(email='moderator@example.com', password='testpassword')
        self.user_owner = User.objects.create(email='owner@example.com', password='testpassword')
        self.user_not_moderator = User.objects.create(email='notmoderator@example.com', password='testpassword')

        # Создание курса
        self.course = Course.objects.create(name='Test Course 1', description='Test description 1', owner=self.user_owner)

        # Создание уроков
        self.lesson1 = Lesson.objects.create(name='Lesson 1', description='Lesson description 1', course=self.course, owner=self.user_owner)
        self.lesson2 = Lesson.objects.create(name='Lesson 2', description='Lesson description 2', course=self.course, owner=self.user_owner)

    def test_crud_lessons(self):
        """
        Проверка CRUD операций с уроками.
        """
        # Авторизация пользователя с правами владельца курса и уроков
        self.client.force_authenticate(user=self.user_owner)

        # Создание нового урока с указанием существующего курса
        response = self.client.post('/lesson/create/', {'name': 'New Lesson',
                                                        'description': 'New Lesson description', 'course': self.course.id})

        # Проверка успешного создания урока
        self.assertEqual(response.status_code, 201,
                         f"Expected status code 201, but got {response.status_code}. Response data: {response.data}")

        # Получение списка уроков
        response = self.client.get('/lesson/')
        self.assertEqual(response.status_code, 200)

        # Проверка, что созданный урок есть в списке
        lesson_name = 'New Lesson'
        lessons = response.data['results']
        lesson_exists = any(lesson['name'] == lesson_name for lesson in lessons)
        self.assertTrue(lesson_exists, f"Lesson '{lesson_name}' not found in the list of lessons")

        # Получение id созданного урока
        lesson_id = response.data['results'][0]['id']

        # Обновление урока
        response = self.client.put(f'/lesson/update/{lesson_id}/',
                                   {'name': 'Updated Lesson', 'description': 'Updated description',
                                    'course': self.course.id})

        # Проверка успешного обновления урока
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Updated Lesson')

        # Удаление урока
        response = self.client.delete(f'/lesson/destroy/{lesson_id}/')

        # Проверка успешного удаления урока
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Lesson.objects.filter(id=lesson_id).exists())

    def test_subscription(self):
        """
        Проверка функционала подписки на курс.
        """
        # Авторизация пользователя не модератора
        self.client.force_authenticate(user=self.user_not_moderator)

        # Подписка на курс
        response = self.client.post('/subscription/', {'course_id': self.course.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'Подписка добавлена')

        # Проверка, что подписка существует
        self.assertTrue(CourseSubscription.objects.filter(user=self.user_not_moderator, course=self.course).exists())

        # Повторная подписка на тот же курс должна удалить подписку
        response = self.client.post('/subscription/', {'course_id': self.course.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'Подписка удалена')
        self.assertFalse(CourseSubscription.objects.filter(user=self.user_not_moderator, course=self.course).exists())

        # Проверка, что невозможно создать подписку без указания ID курса
        response = self.client.post('/subscription/', {})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['message'], 'ID курса не указан')

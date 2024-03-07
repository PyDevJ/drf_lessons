from rest_framework import viewsets, generics, views, response
from rest_framework.permissions import IsAuthenticated, AllowAny

from lms.models import Course, Lesson, CourseSubscription
from lms.serializers import CourseSerializer, LessonSerializer, CourseSubscriptionSerializer
from users.permissions import IsModerator, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def perform_create(self, serializer):
        # При создании курса добавляет текущего пользователя как владельца
        new_course = serializer.save(owner=self.request.user)
        new_course.save()

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='moders').exists():
            # Если пользователь является модератором, показывает все курсы
            return Course.objects.all()
        elif user.is_authenticated:
            # Если пользователь аутентифицирован, показывает только его курсы
            return Course.objects.filter(owner=user)
        else:
            # Если пользователь не аутентифицирован, показывает пустой список
            return Course.objects.none()

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.action in ('update', 'retrieve',):
            self.permission_classes = [IsAuthenticated, IsOwner | IsModerator]
        elif self.action == 'destroy':
            self.permission_classes = [IsAuthenticated, IsOwner]
        return super().get_permissions()


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]

    def perform_create(self, serializer):
        # При создании урока добавляет текущего пользователя как владельца
        new_lesson = serializer.save(owner=self.request.user)
        new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='moders').exists():
            # Если пользователь является модератором, показывает все уроки
            return Lesson.objects.all()
        elif user.is_authenticated:
            # Если пользователь аутентифицирован, показывает только его уроки
            return Lesson.objects.filter(owner=user)
        else:
            # Если пользователь не аутентифицирован, показывает пустой список
            return Lesson.objects.none()


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]


class LessonUpdateAPIView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class SubscriptionAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Получает пользователя
        user = request.user
        # Получает id курса
        course_id = request.data.get('course_id')
        # Проверяет, передан ли идентификатор курса в запросе
        if not course_id:
            return response.Response({"message": "ID курса не указан"}, status=400)
        # Получает объект курса из базы данных
        course = generics.get_object_or_404(Course, id=course_id)
        # Проверяет, существует ли уже подписка у пользователя на этот курс
        subs_item = CourseSubscription.objects.filter(user=user, course=course)
        # Если подписка у пользователя на этот курс есть, то удаляет её
        if subs_item.exists():
            subs_item.delete()
            message = 'Подписка удалена'
        # Если подписки у пользователя на этот курс нет, то создает её
        else:
            CourseSubscription.objects.create(user=user, course=course)
            message = 'Подписка добавлена'
        # Возвращает ответ в API
        return response.Response({"message": message})


class CourseSubscriptionListAPIView(generics.ListAPIView):
    serializer_class = CourseSubscriptionSerializer

    def get_queryset(self):
        return CourseSubscription.objects.filter(user=self.request.user)

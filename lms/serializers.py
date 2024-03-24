from rest_framework import serializers
from lms.models import Course, Lesson, CourseSubscription
from lms.validators import YouTubeLinkValidator


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [
            YouTubeLinkValidator(field='video_link')
        ]


class CourseSerializer(serializers.ModelSerializer):
    count_lessons = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    # Добавляет поле для указания подписки пользователя на курс
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        # fields = '__all__'
        fields = [
            'id',
            'name',
            'updated_at',
            'preview',
            'description',
            'owner',
            'is_subscribed',
            'count_lessons',
            'lessons',
            'price'
        ]

    def get_count_lessons(self, instance):
        return instance.lessons.count()

    def get_is_subscribed(self, obj):
        # Получает текущего пользователя
        user = self.context['request'].user
        # Проверяет, подписан ли текущий пользователь на данный курс
        if user.is_authenticated:
            return CourseSubscription.objects.filter(user=user, course=obj).exists()
        return False


class CourseSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseSubscription
        fields = '__all__'
        # fields = ['id', 'user', 'course']

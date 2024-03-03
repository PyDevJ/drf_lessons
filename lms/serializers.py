from rest_framework import serializers
from lms.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    count_lessons = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        # fields = '__all__'
        fields = [
            'id',
            'name',
            'preview',
            'description',
            'owner',
            'count_lessons',
            'lessons'
        ]

    def get_count_lessons(self, instance):
        return instance.lessons.count()

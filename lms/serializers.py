from rest_framework import serializers
from lms.models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    count_lessons = serializers.SerializerMethodField()

    class Meta:
        model = Course
        # fields = '__all__'
        fields = [
            'id',
            'name',
            'description',
            'count_lessons'
        ]

    def get_count_lessons(self, instance):
        return instance.lesson_set.count()


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'

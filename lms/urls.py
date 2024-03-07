from django.urls import path
from rest_framework import routers
from lms.apps import LmsConfig
from lms.views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView, SubscriptionAPIView, CourseSubscriptionListAPIView

app_name = LmsConfig.name

router = routers.DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')

urlpatterns = [
    path('lesson/create/', LessonCreateAPIView.as_view(), name='create_lesson'),
    path('lesson/', LessonListAPIView.as_view(), name='all_lessons'),
    path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='view_lesson'),
    path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='update_lesson'),
    path('lesson/destroy/<int:pk>/', LessonDestroyAPIView.as_view(), name='delete_lesson'),
    path('subscription/', SubscriptionAPIView.as_view(), name='subscription'),
    path('subs_list/', CourseSubscriptionListAPIView.as_view(), name='subs_list'),
    ] + router.urls

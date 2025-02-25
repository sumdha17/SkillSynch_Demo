from api.v1.serealizers.lesson_serializer import LessonSerializer
from rest_framework.viewsets import ModelViewSet
from course.models import Lesson


class LessonViewSet(ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    authentication_classes = []
    permission_classes = []
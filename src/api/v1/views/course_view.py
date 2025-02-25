from api.v1.serealizers.course_serializer import CourseSerializer
from rest_framework.viewsets import ModelViewSet
from course.models import Course


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    authentication_classes = []
    permission_classes = []
from api.v1.serealizers.que_option_serializer import QuestionOptionSerializer
from rest_framework.viewsets import ModelViewSet
from course.models import QuestionOptions


class QuestionOptionsViewSet(ModelViewSet):
    queryset = QuestionOptions.objects.all()
    serializer_class = QuestionOptionSerializer
    authentication_classes = []
    permission_classes = []
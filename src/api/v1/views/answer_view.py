from api.v1.serealizers.answer_serializer import AnswerSerializer
from rest_framework.viewsets import ModelViewSet
from course.models import Answer


class AnswerViewSet(ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    authentication_classes = []
    permission_classes = []
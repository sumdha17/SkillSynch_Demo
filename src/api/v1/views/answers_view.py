from api.v1.serealizers.answer_serializer import AnswerSerializer
from rest_framework.viewsets import ModelViewSet
from course.models import Answers
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated



class AnswerViewSet(ModelViewSet):
    queryset = Answers.objects.all()
    serializer_class = AnswerSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
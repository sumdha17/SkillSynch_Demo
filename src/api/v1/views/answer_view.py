from api.v1.serealizers.answer_serializer import AnswerSerializer
from rest_framework.viewsets import ModelViewSet
from course.models import Answer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated



class AnswerViewSet(ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
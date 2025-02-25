from api.v1.serealizers.que_option_serializer import QuestionOptionSerializer
from rest_framework.viewsets import ModelViewSet
from course.models import QuestionOptions
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated



class QuestionOptionsViewSet(ModelViewSet):
    queryset = QuestionOptions.objects.all()
    serializer_class = QuestionOptionSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
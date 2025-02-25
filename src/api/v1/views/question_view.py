from api.v1.serealizers.course_question_seriaizer import QuestionSerializer
from rest_framework.viewsets import ModelViewSet
from course.models import Question


class QuestionViewSet(ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    authentication_classes = []
    permission_classes = []
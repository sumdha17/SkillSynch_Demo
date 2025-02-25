from rest_framework import serializers
from course.models import Question

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["id", "module", "question", "type"]
        
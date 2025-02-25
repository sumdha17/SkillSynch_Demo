from rest_framework import serializers
from course.models import Answer

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ["id", "question", "answer", "is_correct"]
        
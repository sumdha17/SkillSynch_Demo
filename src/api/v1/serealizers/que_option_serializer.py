from rest_framework import serializers
from course.models import QuestionOptions

class QuestionOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionOptions
        fields = ["id", "question", "options"]
        
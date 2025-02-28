from rest_framework import serializers
from course.models import Answers

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answers
        fields = ["id", "question", "options"]
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['question'] = str(instance.question.question) if instance.question else None  
        return data
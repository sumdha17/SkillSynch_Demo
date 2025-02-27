from rest_framework import serializers
from course.models import QuestionOptions

class QuestionOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionOptions
        fields = ["id", "question", "options"]
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['question'] = str(instance.question.question) if instance.question else None  
        return data
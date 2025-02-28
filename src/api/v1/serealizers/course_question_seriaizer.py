from rest_framework import serializers
from course.models import Question

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["id", "module", "question", "answer_type"]
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['module'] = str(instance.module.module_number) if instance.module else None  
        data['answer_type'] = str(instance.answer_type.choice_name) if instance.answer_type else None  
        return data
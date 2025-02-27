from rest_framework import serializers
from course.models import Question

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["id", "module", "question", "type"]
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['module'] = str(instance.module.module_number) if instance.module else None  
        data['type'] = str(instance.type.choice_name) if instance.type else None  
        return data
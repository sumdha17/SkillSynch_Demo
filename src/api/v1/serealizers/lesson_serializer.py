from rest_framework import serializers
from course.models import Lesson

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ["id","module", "lesson_number", "lesson_name", "lesson_duration"]
        
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Convert Module (ForeignKey) to its name
        data['module'] = str(instance.module.module_number) if instance.module else None  
        return data
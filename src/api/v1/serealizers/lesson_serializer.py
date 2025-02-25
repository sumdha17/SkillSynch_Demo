from rest_framework import serializers
from course.models import Lesson

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ["id", "lesson_number", "lesson_name", "module", "lesson_duration"]
        
    
    
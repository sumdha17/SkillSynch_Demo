from rest_framework import serializers
from course.models import Lesson

class LessonSerializer(serializers.ModelSerializer):
    lesson_duration = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ["lesson_number", "lesson_name", "module", "lesson_duration"]

    def get_lesson_duration(self, obj):
        return obj.lesson_duration.total_seconds() // 60            # Convert to minutes
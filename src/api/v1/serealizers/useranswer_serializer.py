from rest_framework import serializers
from course.models import UserAnswer
class UserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswer
        fields = ['id', 'user', 'answer', 'user_answer']
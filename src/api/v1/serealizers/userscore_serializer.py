from rest_framework import serializers
from course.models import UserScore

class UserScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserScore
        fields = ['id', 'user', 'lesson', 'attempts', 'score_achieved', 'test_result']

from rest_framework import serializers
from course.models import Assignee

class AssigneeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Assignee
        fields = ["id", "course", "user", "type", "designation", "department", "grade"]
        


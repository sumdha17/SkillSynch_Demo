from rest_framework import serializers
from course.models import Assignee

class AssigneeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Assignee
        fields = ['course', 'user']
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['course'] = str(instance.course.course_title) if instance.course else None
        data['user'] = f"{instance.user.first_name} {instance.user.last_name}" if instance.user else None
        return data
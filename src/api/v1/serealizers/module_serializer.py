from rest_framework import serializers
from course.models import Module

class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['id', 'module_number', 'module_name', 'course']
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
    # Convert course (ForeignKey) to its name
        data['course'] = str(instance.course.course_title)  if instance.course else None
        return data
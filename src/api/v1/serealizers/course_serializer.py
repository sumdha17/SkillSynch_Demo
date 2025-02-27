from rest_framework import serializers
from course.models import Course, Assignee

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id','course_title', 'is_mandatory', 'category', 'no_of_assignee','course_duration','status']
        
    def to_representation(self, instance):
            data = super().to_representation(instance)
        # Convert category (ForeignKey) to its name
            data['category'] = str(instance.category.category_name) if instance.category else None  
        # Convert status (ChoiceField) to its display value
            data['status'] = str(instance.status.choice_name) if instance.status else None  # For ChoiceField
            return 
        
        

from rest_framework import serializers
from course.models import Course

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id','course_title', 'is_mandatory', 'category','status']
        
    def to_representation(self, instance):
            data = super().to_representation(instance)
        # Convert category (ForeignKey) to its name
            data['category'] = str(instance.category.category_name) if instance.category else None  
        # Convert status (ChoiceField) to its display value
            data['status'] = str(instance.status.choice_name) if instance.status else None  # For ChoiceField
            return data
        

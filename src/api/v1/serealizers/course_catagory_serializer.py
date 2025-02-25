from rest_framework import serializers
from course.models import Category

class CatagorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name']
        
        
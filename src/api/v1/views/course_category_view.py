from api.v1.serealizers.course_catagory_serializer import CatagorySerializer
from rest_framework.viewsets import ModelViewSet
from course.models import Category
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CatagorySerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    
    
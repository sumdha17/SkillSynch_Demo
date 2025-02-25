from api.v1.serealizers.course_catagory_serializer import CatagorySerializer
from rest_framework.viewsets import ModelViewSet
from course.models import Category
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CatagorySerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    
    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({'success': f'Category created successfully.'}, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({'success': f'Category deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
    
    
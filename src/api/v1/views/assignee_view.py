from api.v1.serealizers.assignee_serializer import AssigneeSerializer
from rest_framework.viewsets import ModelViewSet
from course.models import Assignee
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from ..peginations.course_pegination import AssigneePagination
from rest_framework.response import Response
from rest_framework import status


class AssigneeViewSet(ModelViewSet):
    queryset = Assignee.objects.all()
    serializer_class = AssigneeSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = AssigneePagination
    
    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({'success': f'Assignee created successfully.'}, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({'success': f'Assignee deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
    
    
    
    
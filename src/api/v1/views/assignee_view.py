from api.v1.serealizers.assignee_serializer import AssigneeSerializer
from rest_framework.viewsets import ModelViewSet
from course.models import Assignee
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from ..peginations.course_pegination import AssigneePagination


class AssigneeViewSet(ModelViewSet):
    queryset = Assignee.objects.all()
    serializer_class = AssigneeSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = AssigneePagination
    
    
    
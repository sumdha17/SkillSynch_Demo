from rest_framework.viewsets import ModelViewSet
from course.models import UserScore
from api.v1.serealizers.userscore_serializer import UserScoreSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


class UserScoreViewSet(ModelViewSet):
    queryset = UserScore.objects.all()
    serializer_class = UserScoreSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({'success': f'UserScore created successfully.'}, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({'success': f'UserScore deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
    
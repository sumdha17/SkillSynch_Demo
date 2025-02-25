from rest_framework.viewsets import ModelViewSet
from course.models import Module
from api.v1.serealizers.module_serializer import ModuleSerializer

class ModuleViewSet(ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    authentication_classes = []
    permission_classes = []
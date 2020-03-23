from rest_framework import viewsets

from .serializers import SideMenuNodeSerializer
from .models import Side_Menu_Node


class SideMenuNodeViewSet(viewsets.ModelViewSet):
    queryset = Side_Menu_Node.objects.all().order_by('name')
    serializer_class = SideMenuNodeSerializer
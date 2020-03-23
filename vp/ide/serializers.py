from rest_framework import serializers

from .models import Side_Menu_Node

class SideMenuNodeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=Side_Menu_Node
        fields=('name', 'type')
from rest_framework import serializers

from .models import Side_Menu_Node, User_Menu_Access


class SideMenuNodeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=Side_Menu_Node
        fields=['name', 'type']

class UserMenuAccessSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=User_Menu_Access
        fields=['user', 'nodeName']
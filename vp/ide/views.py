from rest_framework import viewsets

from .serializers import SideMenuNodeSerializer, UserMenuAccessSerializer
from .models import Side_Menu_Node, User_Menu_Access
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

@csrf_exempt
def snippet_list(request):
    if request.method =='GET':
        """
        Retrieve all nodes in the system.
        """
        queryset = Side_Menu_Node.objects.all().order_by('name')
        serializer = SideMenuNodeSerializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)

@csrf_exempt
def retrieve_nodes_for_user(request, user_id):
    if request.method =='GET':
        """
        Retrieve all nodes that a user can have access to in the IDE.
        """
        try:
            queryset = User_Menu_Access.objects.filter(user=user_id)
        except User_Menu_Access.DoesNotExist:
            return HttpResponse(status=404)

        serializer = UserMenuAccessSerializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)

import requests
from django import http
from django.http import JsonResponse
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from pyworkflow import Node
from modulefinder import ModuleFinder
from django.views.generic import TemplateView
from django.conf import settings
from django.template import engines
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def catchall_dev(request, upstream='http://localhost:3000'):
    """
    Proxy HTTP requests to the frontend dev server in development.

    The implementation is very basic e.g. it doesn't handle HTTP headers.

    """
    upstream_url = upstream + request.path
    method = request.META['REQUEST_METHOD'].lower()
    response = getattr(requests, method)(upstream_url, stream=True)
    content_type = response.headers.get('Content-Type')

    if request.META.get('HTTP_UPGRADE', '').lower() == 'websocket':
        return http.HttpResponse(
            content="WebSocket connections aren't supported",
            status=501,
            reason="Not Implemented"
        )

    elif content_type == 'text/html; charset=UTF-8':
        return http.HttpResponse(
            content=engines['django'].from_string(response.text).render(),
            status=response.status_code,
            reason=response.reason,
        )

    else:
        return http.StreamingHttpResponse(
            streaming_content=response.iter_content(2 ** 12),
            content_type=content_type,
            status=response.status_code,
            reason=response.reason,
        )


catchall_prod = TemplateView.as_view(template_name='index.html')

catchall = catchall_dev if settings.DEBUG else catchall_prod


@swagger_auto_schema(method='get', responses={200:'JSON response with data'})
@api_view(['GET'])
def info(request):
    """Retrieve app info.

       Args:
           request: Django request Object

       Returns:
           200 - JSON response with data.
       """
    data = {
        "application": "visual_programming",
        "version": "negative something",
        "about": "super-duper workflows!"
    }
    return JsonResponse(data)


@swagger_auto_schema(method='get',
                     operation_summary='Retrieve a list of installed Nodes',
                     operation_description='Retrieves a list of installed Nodes, in JSON.',
                     responses={
                         200: 'List of installed Nodes, in JSON',
                     })
@api_view(['GET'])
def retrieve_nodes_for_user(request):
    """Assembles list of Nodes accessible to workflows.

    Retrieve a list of classes from the Node module in `pyworkflow`.
    List is split into 'types' (e.g., 'IO' and 'Manipulation') and
    'keys', or individual command Nodes (e.g., 'ReadCsv', 'Pivot').
    """
    data = dict()

    # Iterate through node 'types'
    for parent in Node.__subclasses__():
        key = getattr(parent, "display_name", parent.__name__)
        data[key] = list()

        # Iterate through node 'keys'
        for child in parent.__subclasses__():
            # TODO: check attribute-scope is handled correctly
            child_node = {
                'name': child.name,
                'node_key': child.__name__,
                'node_type': parent.__name__,
                'num_in': child.num_in,
                'num_out': child.num_out,
                'color': child.color or parent.color,
                'doc': child.__doc__,
                'options': {k: v.get_value() for k, v in child.options.items()},
                'option_types': child.option_types,
                'download_result':  getattr(child, "download_result", False)
            }

            data[key].append(child_node)

    return JsonResponse(data)

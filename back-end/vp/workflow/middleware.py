from pyworkflow import Workflow, WorkflowException
from django.http import JsonResponse


class WorkflowMiddleware:
    """ Custom middleware

    https://docs.djangoproject.com/en/3.0/topics/http/middleware/
    """
    def __init__(self, get_response):
        self.get_response = get_response

        # One-time configuration and initialization.

    def __call__(self, request):
        # Code executed each request before view (and later middleware) called

        path = request.path

        if not path.startswith('/workflow/') and not path.startswith('/node/'):
            # Workflow needed only for /workflow and /node routes
            pass
        elif path == '/workflow/open' or path == '/workflow/new':
            # 'open' loads from file upload, 'new' inits new Workflow
            pass
        else:
            # All other cases, load workflow from session
            try:
                request.pyworkflow = Workflow.from_json(request.session)

                # Check if a graph is present
                if request.pyworkflow.graph is None:
                    return JsonResponse({
                        'message': 'A workflow has not been created yet.'
                    }, status=404)
            except WorkflowException as e:
                return JsonResponse({e.action: e.reason}, status=500)

        response = self.get_response(request)

        # Code executed for each request/response after the view is called

        # Request should have 'pyworkflow' attribute, but do not crash if not
        if hasattr(request, 'pyworkflow'):
            # Save Workflow back to session
            request.session.update(request.pyworkflow.to_session_dict())

        return response

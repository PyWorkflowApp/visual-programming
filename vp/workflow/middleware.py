from pyworkflow import Workflow


class WorkflowMiddleware:
    """ Custom middleware

    https://docs.djangoproject.com/en/3.0/topics/http/middleware/
    """
    def __init__(self, get_response):
        self.get_response = get_response

        # One-time configuration and initialization.
        self.workflow = Workflow()

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        return response

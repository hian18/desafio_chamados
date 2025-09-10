from django.utils import translation


class ForcePortugueseMiddleware:
    """Middleware to force Portuguese language for API requests"""
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Force Portuguese for API requests
        if request.path.startswith('/api/'):
            translation.activate('pt-br')
            request.LANGUAGE_CODE = 'pt-br'
        
        response = self.get_response(request)
        return response

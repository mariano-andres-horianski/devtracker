from .utils import get_current_company, set_current_company

class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        if request.user.is_authenticated and request.user.company:
            set_current_company(request.user.company)
        
        response = self.get_response(request)
        
        # Clean up after request
        set_current_company(None)
        return response
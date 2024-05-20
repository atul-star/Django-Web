from django.http import HttpResponse

class CORSMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Set CORS headers
        response['Access-Control-Allow-Origin'] = '*'  # Allow all origins
        response['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'  # Allow specific methods
        response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'  # Allow specific headers
        response['Access-Control-Allow-Credentials'] = 'true'  # Allow credentials (cookies, authorization headers, etc.)

        # Handle preflight OPTIONS request
        if request.method == 'OPTIONS':
            response['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'  # Allow specific methods for preflight
            return response

        return response

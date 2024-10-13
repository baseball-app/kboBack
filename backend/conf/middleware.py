class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Do stuff
        print(f"Request: {request.method}")

        response = self.get_response(request)

        # Do more stuff
        print(f"Response: {response.status_code}")

        return response

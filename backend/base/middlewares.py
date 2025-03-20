import sentry_sdk


class SentryTransactionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        with sentry_sdk.start_transaction(op="http.request", name=request.path):
            response = self.get_response(request)
            return response

import sentry_sdk


class SentryTransactionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        with sentry_sdk.start_transaction(op="http.request", name=request.path):
            post_data = None
            if request.method in ["POST", "PUT", "PATCH"]:
                try:
                    post_data = request.body.decode("utf-8")
                except Exception:
                    post_data = "[Unreadable]"

            sentry_sdk.set_context("request", {
                "method": request.method,
                "url": request.build_absolute_uri(),
                "headers": dict(request.headers),
                "post_data": post_data,
            })

            response = self.get_response(request)
            return response

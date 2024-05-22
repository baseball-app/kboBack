import os

bind = "0.0.0.0:8000"
wsgi_app = os.path.join(os.path.dirname(__file__), "kboBack", "wsgi.py")

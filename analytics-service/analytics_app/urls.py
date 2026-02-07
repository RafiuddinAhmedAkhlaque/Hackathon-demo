from django.urls import path

urlpatterns = [
    path("health/", lambda r: __import__("django.http", fromlist=["JsonResponse"]).JsonResponse(
        {"status": "healthy", "service": "analytics-service"}
    )),
]


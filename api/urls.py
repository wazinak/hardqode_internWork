from django.urls import include, path

app_name = 'api'

urlpatterns = [
    path('api/v1/', include('api.v1.urls')),
    path("api-auth/", include("rest_framework.urls")),
]

from django.contrib import admin
from django.urls import path, re_path, include

from django.views.generic import TemplateView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
]

schema_view = get_schema_view(
    openapi.Info(
        title="Foodgram API",
        default_version='v1',
        description="Документация для приложения foodgram",
        contact=openapi.Contact(email="foodgram@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns += [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0),
            name='schema-swagger-ui'),
]
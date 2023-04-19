from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, LoginViewset, LogoutViewset

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet, basename='users')

login = LoginViewset.as_view()
logout = LogoutViewset.as_view()

urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/token/login/', login, name='login'),
    path('auth/token/logout/', logout, name='logout'),
]

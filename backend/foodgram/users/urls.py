from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, LoginViewset, LogoutViewset

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet, basename='users')


login = LoginViewset.as_view()
logout = LogoutViewset.as_view()

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/token/login/', login, name='login'),
    path('v1/auth/token/logout/', logout, name='logout'),
]

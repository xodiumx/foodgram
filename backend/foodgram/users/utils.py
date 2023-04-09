from django.core.mail import send_mail
from django.template.loader import get_template
from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    """Получение JWT токенов."""
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
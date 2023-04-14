from rest_framework_simplejwt.utils import aware_utcnow
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken

from foodgram.celery import app


@app.task
def delete_expired_tokens():
    """
    Функция удаления истекших refresh токенов, запускается в полночь.
    """
    OutstandingToken.objects.filter(expires_at__lte=aware_utcnow()).delete()
    return 'Expired refresh tokens are deleted successfully'
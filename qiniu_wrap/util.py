from qiniu import Auth
from django.conf import settings


q = Auth(settings.QINIU_ACCESS_KEY, settings.QINIU_SECRET_KEY)


def get_token():
    return q.upload_token(settings.QINIU_BUCKET_NAME, expires=600)

import dj_database_url

from survey.settings.base import *


DATABASES = {
    'default': dj_database_url.config()
}

MIDDLEWARE_CLASSES += ("django.middleware.security.SecurityMiddleware",)

CSRF_COOKIE_SECURE = True

X_FRAME_OPTIONS = "DENY"

SESSION_COOKIE_SECURE = True

SECURE_BROWSER_XSS_FILTER = True

SECURE_CONTENT_TYPE_NOSNIFF = True

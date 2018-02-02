import dj_database_url

from survey.settings.base import *


DATABASES = {
    'default': dj_database_url.config()
}

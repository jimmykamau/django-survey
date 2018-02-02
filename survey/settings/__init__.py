import os


current_environment = os.getenv("ENVIRONMENT_SETTINGS")

if current_environment == "PRODUCTION":
    from survey.settings.production import *
elif current_environment == "DEVELOPMENT":
    from survey.settings.development import *
elif current_environment == "TESTING":
    from survey.settings.testing import *

from django.apps import AppConfig


class ContentAppConfig(AppConfig):
    """
    Django AppConfig for the content_app application.

    Sets the default primary key field type and imports signal
    handlers when the app is ready to ensure video-related
    post-save and post-delete actions are registered.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "content_app"

    def ready(self):
        from .api import signals

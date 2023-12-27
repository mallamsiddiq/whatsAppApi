from django.apps import AppConfig


class ChatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chat'
    models_module = 'chat.entity.models'

    def ready(self):
        import chat.service.signals

from django.apps import AppConfig

class YourAppConfig(AppConfig):
    name = 'FirebaseStorage'  # ??? ??????? ???

    def ready(self):
        import FirebaseStorage.signals 
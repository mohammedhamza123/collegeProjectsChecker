from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)

class NotificationsConfig(AppConfig):
    name = "notifications"

    def ready(self):
        from .views import FirebaseNotificationService
        firebase_service = FirebaseNotificationService()
        firebase_service.initialize()
        logger.info("✅ Firebase initialized in AppConfig.ready()")



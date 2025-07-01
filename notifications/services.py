from firebase_admin import credentials, initialize_app, messaging
from pathlib import Path
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class FirebaseNotificationService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FirebaseNotificationService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self.app = None
            self._initialized = True
            self.initialize()  # تهيئة تلقائية

    def initialize(self):
        if self.app is not None:
            return  # تم التهيئة مسبقًا
        service_account_path = getattr(settings, "FIREBASE_SERVICE_ACCOUNT_KEY_PATH", None)
        if not service_account_path:
            raise ValueError("FIREBASE_SERVICE_ACCOUNT_KEY_PATH not set in settings.")

        key_path = Path(service_account_path)
        if not key_path.exists():
            raise FileNotFoundError(f"Firebase service account key file not found at {key_path}")

        cred = credentials.Certificate(str(key_path))
        self.app = initialize_app(cred)
        logger.info("✅ Firebase initialized successfully")

    def send_notification(self, token: str, title: str, body: str, data: dict = None):
        if self.app is None:
            raise RuntimeError("Firebase app is not initialized. Call `initialize()` first.")

        try:
            message = messaging.Message(
                notification=messaging.Notification(title=title, body=body),
                token=token,
                data=data or {},
            )
            response = messaging.send(message, app=self.app)
            logger.info(f"✅ Successfully sent message: {response}")
            return response
        except Exception as e:
            logger.error(f"❌ Failed to send notification: {e}")
            raise  # أعد الاستثناء ليظهر في الـ View

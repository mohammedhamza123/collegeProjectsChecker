import os
import json
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
        
        # Try to get Firebase credentials from environment variable first
        firebase_key_json = os.environ.get('FIREBASE_SERVICE_ACCOUNT_KEY')
        
        if firebase_key_json:
            try:
                # Parse JSON from environment variable
                firebase_key_dict = json.loads(firebase_key_json)
                cred = credentials.Certificate(firebase_key_dict)
                self.app = initialize_app(cred)
                logger.info("✅ Firebase initialized successfully from environment variable")
                return
            except (json.JSONDecodeError, Exception) as e:
                logger.warning(f"Failed to parse Firebase key from environment: {e}")
        
        # Fallback to file path method
        service_account_path = getattr(settings, "FIREBASE_SERVICE_ACCOUNT_KEY_PATH", None)
        if not service_account_path:
            raise ValueError("FIREBASE_SERVICE_ACCOUNT_KEY_PATH not set in settings and FIREBASE_SERVICE_ACCOUNT_KEY environment variable not found.")

        key_path = Path(service_account_path)
        if not key_path.exists():
            raise FileNotFoundError(f"Firebase service account key file not found at {key_path}")

        cred = credentials.Certificate(str(key_path))
        self.app = initialize_app(cred)
        logger.info("✅ Firebase initialized successfully from file")

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

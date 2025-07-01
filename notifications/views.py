"""

    token = "fX538NtEQtacQe5CcUx2cN:APA91bGAkmDcpEUHAKRtNiHfxYnTU7z42KroVAcaJpkJNG3L-symlDe7Euu_t8QdECaF0jni4RYHYiU5MFhkKScDE0T902yYG1W0gSWBY2nhI15taX5nPSM"
"""




from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from notifications.services import FirebaseNotificationService

class NotificationViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=["post"])
    def send(self, request):
        token = request.data.get("token")
        title = request.data.get("title")
        body = request.data.get("body")
        data = request.data.get("data", {})

        if not token or not title or not body:
            return Response({"error": "token, title, and body are required."}, status=status.HTTP_400_BAD_REQUEST)

        firebase_service = FirebaseNotificationService()
        try:
            response = firebase_service.send_notification(
                token=token,
                title=title,
                body=body,
                data=data
            )
            return Response({"message": "Notification sent successfully ✅", "response": response})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

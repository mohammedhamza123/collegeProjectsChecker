from rest_framework.serializers import ModelSerializer
from .models import Messege, Channel
from login.serializers import UserSerializer

class MesssegeSerializer(ModelSerializer):
    sender = UserSerializer()
    class Meta:
        model = Messege
        fields = "__all__"


class ChannelSerializer(ModelSerializer):
    class Meta:
        model = Channel
        fields = "__all__"


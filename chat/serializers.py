from rest_framework.serializers import ModelSerializer
from .models import Messege, Channel
from login.serializers import UserSerializer

class MesssegeSerializer(ModelSerializer):
    class Meta:
        model = Messege
        fields = "__all__"


class ChannelSerializer(ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Channel
        fields = "__all__"


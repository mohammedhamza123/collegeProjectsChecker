from django.shortcuts import render ,get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import *
from django.contrib.auth.models import User,Group


class MessegeViewSet(ModelViewSet):
    """
    MessegesModel views
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = MesssegeSerializer
    queryset = Messege.objects.all()

    def list(self, request, *args, **kwargs):
        try:
            channel = int(request.query_params["channel"][0])
        except Exception:
            queryset = []
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        queryset = self.queryset.filter(Channel=channel)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({"datum", serializer.data})


class ChannelViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChannelSerializer
    queryset = Channel.objects.all()

    def list(self, request, *args, **kwargs):
        user = get_object_or_404(User,id=request.user)
        user_group = Group.objects.filter(user=user.id).first()
        queryset = self.queryset.filter(members=request.user.id)
        if user_group.name == "admin":
            queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({"datum": serializer.data})

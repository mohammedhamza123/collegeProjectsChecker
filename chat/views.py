from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import *


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
        return Response(serializer.data)


class ChannelViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChannelSerializer
    queryset = Channel.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.filter(members=request.user.id)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

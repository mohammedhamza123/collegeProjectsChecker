from django.shortcuts import render ,get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from .serializers import *
from django.contrib.auth.models import User,Group
from api.models import Project ,Student


class MessegeViewSet(ModelViewSet):
    """
    MessegesModel views
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = MesssegeSerializer
    queryset = Messege.objects.all()

    def list(self, request, *args, **kwargs):
        user = get_object_or_404(User,id=request.user.id)
        user_group = Group.objects.filter(user=user.id).first()
        channel_query = request.query_params.get('channel')
        if channel_query:
            channel = get_object_or_404(Channel,id=int(channel_query),members=user.id)
            queryset = self.queryset.filter(id=int(channel_query))
        else:
            if user_group:
                if user_group.name == "admin" or user_group == "teacher":
                    queryset = self.filter_queryset(self.get_queryset())
                elif user_group.name == "student":
                    student = get_object_or_404(Student,id=user.id)
                    channel = Channel.objects.filter(project=student.project).first()
                    queryset = self.queryset.filter(channel=channel.id)
            else:
                raise NotFound(detail="Error 404, page not found", code=404)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({"datum":serializer.data})


class ChannelViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChannelSerializer
    queryset = Channel.objects.all()

    def list(self, request, *args, **kwargs):
        user = get_object_or_404(User,id=request.user.id)
        user_group = Group.objects.filter(user=user.id).first()
        queryset = self.queryset.filter(members=request.user.id)
        if user_group:
            if user_group.name == "admin":
                queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({"datum": serializer.data})

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .serializers import *

# Create your views here.


class TeacherViewSet(viewsets.ModelViewSet):
    """
    TeacherModel View.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = TeacherSerializer
    queryset = Teacher.objects.all()


class StudentViewSet(viewsets.ModelViewSet):
    """
    StudentModel View.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = StudentSerializer
    queryset = Student.objects.all()


class ProjectViewSet(viewsets.ModelViewSet):
    """
    ProjectModel View.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()


class ImportantDateViewSet(viewsets.ModelViewSet):
    """
    ImportantDateModel View.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = ImportantDateSerializer
    queryset = ImportantDate.objects.all()


class RequirementViewSet(viewsets.ModelViewSet):
    """
    RequiremenetModel View.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = RequirementSerializer
    queryset = Requirement.objects.all()


class SuggestionViewSet(viewsets.ModelViewSet):
    """
    SuggestionModel View.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = SuggestionSerializer
    queryset = Suggestion.objects.all()

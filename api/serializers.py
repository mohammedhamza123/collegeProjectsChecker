from .models import *
from login.serializers import UserSerializer
from rest_framework import serializers


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"


class StudentDetailsSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Use the UserSerializer for the related User model

    class Meta:
        model = Student
        fields = "__all__"  # Add the desired fields


class SuggestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suggestion
        fields = "__all__"


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = "__all__"


class TeacherDetailsSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Use the UserSerializer for the related User model

    class Meta:
        model = Teacher
        fields = "__all__"


class ImportantDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportantDate
        fields = "__all__"


class RequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requirement
        fields = "__all__"


class ProjectDetailsSerializer(serializers.ModelSerializer):
    teacher = TeacherDetailsSerializer()
    main_suggestion = SuggestionSerializer()

    class Meta:
        model = Project
        fields = "__all__"

class APIKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = APIKey
        fields = "__all__"

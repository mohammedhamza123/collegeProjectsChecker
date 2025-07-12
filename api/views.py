from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets , status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import Response
from django.contrib.auth.models import Group
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .models import Project

from .serializers import *

# Create your views here.


class TeacherViewSet(viewsets.ModelViewSet):
    """
    TeacherModel View.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = TeacherSerializer
    queryset = Teacher.objects.all()

    def list(self, request, *args, **kwargs):
        if not request.query_params:
            queryset = self.filter_queryset(self.get_queryset())
        else:
            try:
                user = int(request.query_params.get("user"))
                queryset = self.queryset.filter(user=user)
            except:
                pass

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({"datum": serializer.data})


class TeacherDetailsViewSet(viewsets.ModelViewSet):
    """
    TeacherModel View.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = TeacherDetailsSerializer
    queryset = Teacher.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({"datum": serializer.data})

    

class StudentViewSet(viewsets.ModelViewSet):
    """
    StudentModel View.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = StudentSerializer
    queryset = Student.objects.all()

    def list(self, request, *args, **kwargs):
        
        if not request.query_params:
            queryset = self.filter_queryset(self.get_queryset())
        else:
            try:
                user = int(request.query_params.get("user"))
                queryset = self.queryset.filter(user=user)
                # Check if student is approved
                if queryset.exists():
                    student = queryset.first()
                    if not student.is_approved:
                        return Response(
                            {"error": "Student account is not approved yet"}, 
                            status=403
                        )
            except:
                pass

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({"datum": serializer.data})

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """موافقة الإدارة على الطالب"""
        student = self.get_object()
        student.is_approved = True
        student.save()
        return Response({"status": "تمت الموافقة على الطالب بنجاح"})

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """رفض الطالب من قبل الإدارة وحذفه من قاعدة البيانات"""
        student = self.get_object()
        
        # حفظ معلومات الطالب قبل حذفه
        student_name = f"{student.user.first_name} {student.user.last_name}"
        student_username = student.user.username
        
        # حذف الطالب من قاعدة البيانات (الإشارة ستتعامل مع حذف المستخدم تلقائياً)
        student.delete()
        
        return Response({
            "status": "تم رفض الطالب وحذفه من النظام",
            "student_name": student_name,
            "student_username": student_username
        })

    @action(detail=False, methods=['get'])
    def pending_approval(self, request):
        """قائمة الطلاب الذين ينتظرون الموافقة"""
        queryset = self.queryset.filter(is_approved=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response({"datum": serializer.data})


class StudentDetailsViewSet(viewsets.ModelViewSet):
    """
    StudentModel View.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = StudentDetailsSerializer
    queryset = Student.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({"datum": serializer.data})


class ProjectViewSet(viewsets.ModelViewSet):
    """
    ProjectModel View.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        # student = get_object_or_404(Student, user=request.user)
        # project = student.project
        # queryset = self.queryset.filter(id=project.id)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({"datum": serializer.data})

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.calculate_progression()
        instance.calculate_final_score_and_status()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ProjectDetailsViewSet(viewsets.ModelViewSet):
    """
    ProjectModel View.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = ProjectDetailsSerializer
    queryset = Project.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        # student = get_object_or_404(Student, user=request.user)
        # project = student.project
        # queryset = self.queryset.filter(id=project.id)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({"datum": serializer.data})

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.calculate_progression()
        instance.calculate_final_score_and_status()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ImportantDateViewSet(viewsets.ModelViewSet):
    """
    ImportantDateModel View.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = ImportantDateSerializer
    queryset = ImportantDate.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.queryset
        user_group = Group.objects.filter(user=request.user).first()
        if not user_group == None:
            if user_group.name == "student":
                student = get_object_or_404(Student, user=request.user)
                queryset = self.queryset.filter(project=student.project)
            elif user_group.name == "teacher":
                teacher = get_object_or_404(Teacher, user=request.user)
                queryset = self.queryset.filter(teacher=teacher.id)
        else:
            queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({"datum": serializer.data})


class RequirementViewSet(viewsets.ModelViewSet):
    """
    RequiremenetModel View.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = RequirementSerializer
    queryset = Requirement.objects.all()

    def list(self, request, *args, **kwargs):
        # queryset = self.filter_queryset(self.get_queryset())
        if not request.query_params:
            queryset = self.filter_queryset(self.get_queryset())
        else:
            try:
                suggestion = int(request.query_params.get("suggestion"))
                queryset = self.queryset.filter(suggestion=suggestion)
            except:
                return Response(
                    status=404, data={"details": "incorrect query parameters"}
                )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({"datum": serializer.data})


class SuggestionViewSet(viewsets.ModelViewSet):
    """
    SuggestionModel View.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = SuggestionSerializer
    queryset = Suggestion.objects.all()

    def list(self, request, *args, **kwargs):
        group_name = Group.objects.filter(user=request.user).first()
        if group_name == "student":
            student = get_object_or_404(Student, user=request.user)
            project = student.project
            queryset = self.queryset.filter(project=project.id)
        else:
            queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({"datum": serializer.data})


class APIKeyViewSet(viewsets.ModelViewSet):
    """
    APIKey Singleton ViewSet.
    Only allows retrieving, updating, or deleting the single APIKey instance.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = APIKeySerializer
    queryset = APIKey.objects.all()

    def create(self, request, *args, **kwargs):
        if APIKey.objects.exists():
            return Response(
                {"detail": "Only one APIKey instance allowed."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        instance = APIKey.objects.first()
        if not instance:
            return Response({"detail": "No APIKey instance found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

@action(detail=True, methods=['post'])
def approve_student(self, request, pk=None):
    student = self.get_object()
    # Implement the logic to approve the student
    return Response({"status": "Student approved successfully"})

@action(detail=True, methods=['post'])
def reject_student(self, request, pk=None):
    student = self.get_object()
    # Implement the logic to reject the student
    return Response({"status": "Student rejected successfully"})

class UploadGradePDF(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, project_id):
        project = Project.objects.get(id=project_id)
        pdf_file = request.FILES['file']
        role = request.data.get('role')
        grade = request.data.get('grade')

        # حفظ ملف PDF في الحقل المناسب
        if role == "examiner1":
            project.pdf_examiner1 = pdf_file
            project.first_grading = grade
        elif role == "examiner2":
            project.pdf_examiner2 = pdf_file
            project.second_grading = grade
        elif role == "supervisor":
            project.pdf_supervisor = pdf_file
            project.supervisor_grade = grade
        elif role == "head":
            project.pdf_head = pdf_file
            project.department_head_grade = grade
        elif role == "coordinator":
            project.pdf_coordinator = pdf_file
            project.coordinator_grade = grade
        else:
            return Response({"error": "دور غير معروف"}, status=status.HTTP_400_BAD_REQUEST)

        project.save()
        return Response({"success": True, "grade": grade})
"""
URL configuration for CheckProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.schemas import get_schema_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from rest_framework.routers import DefaultRouter
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from login.views import UserViewSet, RegisterView, MyAccountView,ChangePasswordView
from api.views import (
    APIKeyViewSet,
    StudentViewSet,
    StudentDetailsViewSet,
    TeacherViewSet,
    TeacherDetailsViewSet,
    ProjectViewSet,
    ProjectDetailsViewSet,
    SuggestionViewSet,
    ImportantDateViewSet,
    RequirementViewSet,
)

from chat.views import MessegeViewSet, ChannelViewSet ,DetialedMessegeViewSet

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", RegisterView.as_view(), name="registeration"),
    path("changePassword/", ChangePasswordView.as_view(), name="change-password"),
    path("myaccount/", MyAccountView.as_view(), name="myAccount"),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # Optional UI:
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]

router = DefaultRouter()
router.register(r"user", UserViewSet, basename="user")
router.register(r"student", StudentViewSet, basename="student")
router.register(r"teacher", TeacherViewSet, basename="teacher")
router.register(r"project", ProjectViewSet, basename="project")
router.register(r"importantDate", ImportantDateViewSet, basename="importantDate")
router.register(r"requirement", RequirementViewSet, basename="requirement")
router.register(r"suggestion", SuggestionViewSet, basename="suggestion")
router.register(r"messages", MessegeViewSet, basename="messege")
router.register(r"detailedMessags", DetialedMessegeViewSet, basename="Detailedmessage")
router.register(r"channel", ChannelViewSet, basename="channel")
router.register(r"studentDetails", StudentDetailsViewSet, basename="studentDetails")
router.register(r"teacherDetails", TeacherDetailsViewSet, basename="teacherDetails")
router.register(r"projectDetails", ProjectDetailsViewSet, basename="projectDetails")
router.register(r"apikey", APIKeyViewSet, basename="apikey")
urlpatterns += router.urls

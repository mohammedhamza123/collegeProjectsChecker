from typing import Any
from django.db import models
from django.conf import settings


class Project(models.Model):
    title = models.CharField(max_length=70)
    image = models.CharField(max_length=200)
    progression = models.FloatField()

    def __str__(self) -> str:
        return self.title

class Suggestion(models.Model):
    STATUSES = (
        ("w", "waiting"),
        ("r", "rejected"),
        ("a", "approved"),
    )
    content = models.TextField()
    # settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    status = models.CharField(max_length=2, null=True, choices=STATUSES, default="w")
    title = models.CharField(max_length=50)
    image = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.title


class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    phoneNumber = models.IntegerField()  # 0914210840

    def __str__(self) -> str:
        return self.user.username


class Teacher(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phoneNumber = models.IntegerField()  # 0914210840

    def __str__(self) -> str:
        return self.user.username


class ImportantDate(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    date_type = models.CharField(max_length=30)
    date = models.DateField()

    def __str__(self) -> str:
        return f"{self.teacher}"


class Requirement(models.Model):
    name = models.CharField(max_length=40)
    suggestion = models.ForeignKey(Suggestion, on_delete=models.CASCADE)

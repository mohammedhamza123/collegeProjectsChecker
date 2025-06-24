from typing import Any
from django.db import models
from django.conf import settings


class Teacher(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phoneNumber = models.IntegerField()  
    isExaminer = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.user.username

class Project(models.Model):
    title = models.CharField(max_length=70)
    image = models.CharField(max_length=200)
    first_grading = models.CharField(max_length=500,null=True,blank=True)
    second_grading = models.CharField(max_length=500,null=True,blank=True)
    teacher_grading = models.CharField(max_length=500,null=True,blank=True)
    progression = models.FloatField()
    main_suggestion = models.OneToOneField(
        "Suggestion",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="project_main_suggestion",
    )
    delivery_date = models.DateField(null=True, blank=True)
    teacher = models.ForeignKey(Teacher,null=True,blank=True,on_delete=models.DO_NOTHING)

    def calculate_progression(self):
        if not self.main_suggestion or self.main_suggestion.status == "i":
            suggestionList = Suggestion.objects.filter(project=self.id, status="a")
            if suggestionList.count() > 0:
                self.main_suggestion = suggestionList.first()
        total_requirements = Requirement.objects.filter(
            suggestion=self.main_suggestion
        ).count()
        completed_requirements = Requirement.objects.filter(
            status="c", suggestion=self.main_suggestion
        ).count()
        if total_requirements > 0:
            self.progression = (completed_requirements / total_requirements) * 100
        else:
            self.progression = 0
        self.save()
        return self.progression

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

    def save(self, *args, **kwargs):
        if self.status == "a":
            # Get the project associated with the suggestion
            project = self.project

            # Check if there is already a main suggestion for the project
            if project.main_suggestion and project.main_suggestion != self:
                # Set the status of the existing main suggestion to "w" (waiting)
                project.main_suggestion.status = "w"
                project.main_suggestion.save()

            # Set the main suggestion for the project to the current suggestion
            project.main_suggestion = self

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title


class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)
    phoneNumber = models.IntegerField(null=True)  # 0914210840
    serialNumber = models.IntegerField(null=True, blank=True)

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
    STATUSES = (
        ("c", "completed"),
        ("i", "incomplete"),
    )
    status = models.CharField(max_length=2, null=True, choices=STATUSES, default="i")

class APIKey(models.Model):
    key = models.CharField(max_length=40, unique=True)
    
    def save(self, *args, **kwargs):
        if not self.pk and APIKey.objects.exists():
            raise Exception("There can be only one APIKey instance")
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.key
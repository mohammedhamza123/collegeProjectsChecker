from django.contrib import admin
from .models import Student, Teacher, Project, ImportantDate, Requirement, Suggestion ,APIKey

# Register your models here.
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Project)
admin.site.register(Suggestion)
admin.site.register(ImportantDate)
admin.site.register(Requirement)
admin.site.register(APIKey)
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.db.models.signals import m2m_changed, post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Student, Teacher, Requirement
from chat.models import Channel
from api.models import Project


@receiver(m2m_changed, sender=Group.user_set.through)
def add_user_to_group_on_change(
    sender, instance, action, reverse, model, pk_set, **kwargs
):
    if action == "post_add" and instance.groups.first().name == "student":
        user = User.objects.get(id=instance.id)
        if not hasattr(user, "student"):
            student = Student.objects.create(user=user, phoneNumber=0, is_approved=False)
    if action == "post_add" and instance.groups.first().name == "teacher":
        user = User.objects.get(id=instance.id)
        if not hasattr(user, "teacher"):
            teacher = Teacher.objects.create(user=user, phoneNumber=0)


@receiver(post_delete, sender=Student)
def delete_user_on_student_delete(sender, instance, **kwargs):
    """حذف المستخدم عند حذف الطالب"""
    try:
        user = instance.user
        # حذف المستخدم من مجموعة الطلاب
        try:
            students_group = Group.objects.get(name='students')
            user.groups.remove(students_group)
        except Group.DoesNotExist:
            pass
        # حذف المستخدم من قاعدة البيانات
        user.delete()
    except User.DoesNotExist:
        pass  # المستخدم محذوف بالفعل


@receiver(post_save, sender=Project)
def create_channel(sender, instance, created, **kwargs):
    if created:
        channel = Channel(project=instance)
        if instance.teacher:
            channel.members.add(instance.teacher)
        channel.save()


@receiver(pre_save, sender=Student)
def update_channel_members(sender, instance, **kwargs):
    try:
        channel = Channel.objects.get(project=instance.project)

        # If the Student instance is being edited and the project field is updated
        # if instance.pk and instance.project != instance.__class__.objects.get(pk=instance.pk).project:
        #     # Remove the student from the previous channel's members list
        #     channel.members.remove(instance)
        channel.members.add(instance.user)

    except Channel.DoesNotExist:
        pass


@receiver(post_save, sender=Project)
def update_channel_teacher(sender, instance, **kwargs):
    if instance.teacher:
        try:
            channel = instance.channel
            channel.members.add(instance.teacher.user)
            channel.save()
        except Channel.DoesNotExist:
            pass
            # channel = Channel()
            # channel.save()


@receiver([post_save, post_delete], sender=Requirement)
def update_project_percentage(sender, instance, **kwargs):
    suggestion = instance.suggestion
    total_requirements = Requirement.objects.filter(suggestion=suggestion).count()
    completed_requirements = Requirement.objects.filter(
        suggestion=suggestion, status="c"
    ).count()
    if total_requirements > 0:
        percentage = (completed_requirements / total_requirements) * 100
    else:
        percentage = 0
    project = suggestion.project_main_suggestion
    project.progression = percentage
    project.save()

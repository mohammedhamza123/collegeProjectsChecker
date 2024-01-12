from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver , pre_save
from .models import Student, Teacher
from chat.models import Channel
from api.models import Project


@receiver(m2m_changed, sender=Group.user_set.through)
def add_user_to_group_on_change(
    sender, instance, action, reverse, model, pk_set, **kwargs
):
    if action == "post_add" and instance.groups.first().name == "student":
        user = User.objects.get(id=instance.id)
        if not hasattr(user, "student"):
            student = Student.objects.create(user=user, phoneNumber=0)
    if action == "post_add" and instance.groups.first().name == "teacher":
        user = User.objects.get(id=instance.id)
        if not hasattr(user, "teacher"):
            teacher = Teacher.objects.create(user=user, phoneNumber=0)


@receiver(post_save, sender=Project)
def create_channel(sender, instance, created, **kwargs):
    if created:
        channel = Channel(project=instance)
        channel.save()

@receiver(pre_save, sender=Student)
def update_channel_members(sender, instance, **kwargs):
    try:
        channel = Channel.objects.get(project=instance.project)

        # If the Student instance is being edited and the project field is updated
        # if instance.pk and instance.project != instance.__class__.objects.get(pk=instance.pk).project:
        #     # Remove the student from the previous channel's members list
        #     channel.members.remove(instance)
        channel.members.add(instance)

    except Channel.DoesNotExist:
        pass

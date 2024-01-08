from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Student ,Teacher

@receiver(m2m_changed, sender=Group.user_set.through)
def add_user_to_group_on_change(sender, instance, action, reverse, model, pk_set, **kwargs):
    if action == 'post_add' and instance.groups.first().name == 'student':
        user = User.objects.get(id=instance.id)
        if not hasattr(user, 'student'):
            student = Student.objects.create(user=user, phoneNumber=0)
    if action == 'post_add' and instance.groups.first().name == 'teacher':
        user = User.objects.get(id=instance.id)
        if not hasattr(user, 'teacher'):
            teacher = Teacher.objects.create(user=user, phoneNumber=0)
            
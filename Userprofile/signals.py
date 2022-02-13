import re
from django.db.models.signals import post_save
from Alluser.models import User
from django.dispatch import receiver
from .models import *

@receiver(post_save,sender=User)
def post_save_create_profile(sender,instance,created,**kwarg):
    if created:
        UserBio.objects.create(id=instance)
@receiver(post_save,sender=Relationship)
def post_save_add_to_friends(sender,created,instance,**kwarg):
    sender_ = instance.sender
    receiver_ = instance.receiver
    if instance.status=='accepted':
        sender_.friends.add(receiver_.id)
        receiver_.friends.add(sender_.id)
        sender_.save()
        receiver_.save()
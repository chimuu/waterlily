from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from account.models import Profile
import logging

logger = logging.getLogger('main')


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


# TODO: make User post_save signals code async
# from account.tasks import create_update_user_profile
#
#
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     logger.info(instance.id)
#     create_update_user_profile.delay(created, instance.id)
#
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     create_update_user_profile.delay(False, instance.id, instance.profile)

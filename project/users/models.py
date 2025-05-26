from django.db import models
from django.contrib.auth.models import User

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    sex = models.CharField(max_length=10, blank=True)
    height = models.FloatField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    notify_email = models.EmailField(blank=True)  # ✅ Add this line

    def __str__(self):
        return f"{self.user.username}'s Profile"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from django.db.models.signals import post_save


class CustomUser(AbstractUser):
    bio = models.TextField(max_length=300, blank=True)
    profile_picture = models.ImageField(blank=True, upload_to='profile_pics/')
    followers = models.ManyToManyField('self', 
        symmetrical=False, 
        related_name='following',
        blank=True,
        )
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

    @property
    def followers_count(self):
        return self.followers.count()
    
    @property
    def following_count(self):
        return self.following.count()
    
@receiver(post_save, sender=CustomUser)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    #short biography disaplayed on profile page
    bio = models.TextField(blank= True, null=True)

    # Profile picture - stored in media/profile_pics/
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    # Self-referential M2M for the follow system
    # symmetrical=False → A follows B does NOT imply B follows A
    # related_name='followers' → user.followers.all() = who follows this user
    # blank=True → a new user starts with no followers/following
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank= True)

    def __str__(self):
        return f"{self.username}"
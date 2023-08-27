from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    creater = models.ForeignKey(User, related_name='my_name', on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    liked = models.ManyToManyField(User, related_name='liked_users_or_post' ,blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.creater} posted {self.content}"
    
class Follow(models.Model):
    following = models.ForeignKey(User, related_name="I_am_following", on_delete=models.CASCADE)
    me = models.ForeignKey(User, related_name="following_me", on_delete=models.CASCADE)
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    creater = models.ForeignKey(User, related_name='my_name', on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    liked = models.ManyToManyField(User, related_name='liked_users_or_post' ,blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(null=True, blank=True, upload_to='images/')
    
    def __str__(self):
        return f"{self.creater} posted {self.content}"
    
class Follow(models.Model):
    following = models.ForeignKey(User, related_name="I_am_following", on_delete=models.CASCADE)
    me = models.ForeignKey(User, related_name="following_me", on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.me} follows {self.following}"
    
class Comment(models.Model):
    commented = models.ForeignKey(Post,on_delete=models.CASCADE, null=True, blank=True, related_name="comments")
    commenter = models.ForeignKey(User, related_name="user_name", on_delete=models.CASCADE, null=True)
    comment = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"{self.commenter} : {self.comment}" 
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date = models.DateTimeField(auto_now=True, editable=True)
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    likes = models.ManyToManyField(User,related_name='blogpost_likes', null = True)
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs=({'pk':self.pk}))

class comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    describ = models.CharField(max_length=50,default='')
    timestamp = models.DateTimeField(auto_now_add=True,editable=True)
    commentor = models.ForeignKey(User, on_delete = models.CASCADE,null = True)
  
    def __str__(self):
        return self.commentor.username

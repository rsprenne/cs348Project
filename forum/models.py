from django.utils import timezone
from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length= 100)
    content = models.TextField(null=True, blank=True)
    author = models.CharField(max_length=200, default = "rspre")
    created_date = models.DateTimeField(default=timezone.now)
    tags = models.ManyToManyField(Tag, related_name='posts')
    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    author = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.content
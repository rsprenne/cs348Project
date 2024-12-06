from django.utils import timezone
from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    db_index = True
                    
    class Meta:
        indexes = [models.Index(fields=['name'])]

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length= 100)
    content = models.TextField(null=True, blank=True)
    author = models.CharField(max_length=200, default = "rspre")
    created_date = models.DateTimeField(default=timezone.now)
    tags = models.ManyToManyField(Tag, related_name='posts')

    # db_index = True

    # class Meta:
    #     indexes = [models.Index(fields=['tags'])]

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
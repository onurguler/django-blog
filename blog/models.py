from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Post(models.Model):
    owner = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=255)
    body = models.TextField()
    published = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%(owner)s - %(created_at)s" % {
            "owner": self.owner.username,
            "created_at": self.created_at
        }

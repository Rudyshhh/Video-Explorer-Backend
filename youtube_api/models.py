
from django.db import models

class Video(models.Model):
    vid = models.CharField(max_length=20, unique=True)  # Video ID
    url = models.URLField()
    title = models.CharField()
    desc = models.TextField()
    likes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    pub_date = models.DateTimeField()
    thumb = models.URLField()

    def __str__(self):
        return self.title

    
class YouTubeVideo(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    vid = models.CharField(max_length=50, unique=True)
    published_at = models.DateTimeField()
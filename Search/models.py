from django.db import models

# Create your models here.

class SearchKeyWord(models.Model):
    ip = models.CharField(max_length=20)
    keyword = models.CharField(max_length=200)

    def __str__(self):
        return self.keyword

class Video(models.Model):
    title = models.TextField()
    description = models.TextField(blank=True, null=True)
    video_url = models.URLField(unique=True)
    thumbnail = models.URLField()
    channel_title = models.CharField(max_length=200)
    pub_date = models.DateTimeField()
    channel_url = models.URLField()
    video_duration = models.DurationField()

    def __str__(self):
        return self.title




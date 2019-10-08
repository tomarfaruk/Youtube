from django.db import models

# Create your models here.

class SearchKeyWord(models.Model):
    ip = models.CharField(max_length=20)
    keyword = models.CharField(max_length=200)

    def __str__(self):
        return self.keyword

# class Video(models.Model):
#     title = models.CharField()
#     description = models.CharField()
#     url = models.URLField()
#     thumbnail = models.CharField()
#     channel_title = models.CharField()
#     pub_date = models.DateTimeField()
#     channel_link = models.URLField()

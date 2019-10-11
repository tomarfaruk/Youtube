from rest_framework import serializers
from .models import Video

class VideoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Video
        fields =['url', 'id', 'title', 'description',
                 'video_url', 'thumbnail', 'channel_title',
                 'pub_date', 'channel_url', 'video_duration'
                 ]

import requests
from isodate import parse_duration
from django.conf import settings
from django.shortcuts import render, redirect
from .models import SearchKeyWord, Video
from .serializers import VideoSerializer
from rest_framework import viewsets, filters


class VideoView(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['title', 'description', ]
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]



def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def index(request):
    videos = []

    if request.method == 'POST':
        if request.POST['submit'] == 'history':
            context = {
                'historys': SearchKeyWord.objects.filter(ip=get_client_ip(request)).order_by('-id')
            }
            return render(request, 'Search/history.html', context)

        search_keyword = request.POST['search'] or 'HOME'
        if search_keyword is not "HOME":
            ip = get_client_ip(request)
            SearchKeyWord.objects.create(ip=ip, keyword=search_keyword).save()

        search_url = 'https://www.googleapis.com/youtube/v3/search'
        video_url = 'https://www.googleapis.com/youtube/v3/videos'

        search_params = {
            'part': 'snippet',
            'q': search_keyword,
            'key': settings.YOUTUBE_DATA_API_KEY,
            'maxResults': 12,
            'type': 'video'
        }

        r = requests.get(search_url, params=search_params)
        # print(r.text)

        results = r.json()['items']

        video_ids = []
        for result in results:
            video_ids.append(result['id']['videoId'])

        if request.POST['submit'] == 'lucky':
            return redirect(f'https://www.youtube.com/watch?v={video_ids[0]}')




        video_params = {
            'key': settings.YOUTUBE_DATA_API_KEY,
            'part': 'snippet,contentDetails',
            'id': ','.join(video_ids),
            'maxResults': 12
        }

        r = requests.get(video_url, params=video_params)
        # print(r.text)

        results = r.json()['items']


        for result in results:
            title = result['snippet']['title']
            video_url = f'https://www.youtube.com/watch?v={result["id"]}'
            pub_date = result['snippet']['publishedAt']
            channel_url = f"https://www.youtube.com/watch?v={result['snippet']['channelId']}"
            channel_title = result['snippet']['channelTitle']
            description = result['snippet']['description']
            thumbnail = result['snippet']['thumbnails']['high']['url']
            duration = result['contentDetails']['duration']
            is_exist = Video.objects.filter(video_url__exact=video_url).exists()
            print('result is ', is_exist)
            if not is_exist:
                Video.objects.create(title=title, video_url=video_url, pub_date=pub_date,
                                     channel_title=channel_title, channel_url=channel_url,
                                     description=description, thumbnail=thumbnail, video_duration=duration)
            # print('title 1', title)
            # print('video url 2', video_url)
            # print('pub date 3', pub_date)
            # print('channel title 4', channel_title)
            # print('channel url 5', channel_url)
            # print('duration 6', duration)
            # print('description 7', description)
            # print('thumbnail 8', thumbnail)

            video_data = {
                'title': result['snippet']['title'],
                'id': result['id'],
                'url': f'https://www.youtube.com/watch?v={result["id"]}',
                'duration': int(parse_duration(result['contentDetails']['duration']).total_seconds() // 60),
                'thumbnail': result['snippet']['thumbnails']['high']['url']
            }

            videos.append(video_data)

    context = {
        'videos': videos
    }

    return render(request, 'Search/index.html', context)
import requests
from isodate import parse_duration
from django.conf import settings
from django.shortcuts import render, redirect
from .models import SearchKeyWord


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
            'maxResults': 10,
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
            'maxResults': 10
        }

        r = requests.get(video_url, params=video_params)
        # print(r.text)

        results = r.json()['items']

        for result in results:
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
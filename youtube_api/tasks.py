# AIzaSyCCdxweLAQcCm7F72H8bQSHikYF_5SCQ3c


from django.conf import settings
import requests
from celery import shared_task
from .models import YouTubeVideo,Video

YOUTUBE_API_KEY = "AIzaSyCCdxweLAQcCm7F72H8bQSHikYF_5SCQ3c"

@shared_task
def fetch_youtube_videos(query, max_results=10):
    search_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&type=video&maxResults={max_results}&key={YOUTUBE_API_KEY}"
    search_response = requests.get(search_url)

    if search_response.status_code != 200:
        return {'error': 'YouTube search API failed', 'details': search_response.text}

    videos = search_response.json().get('items', [])

    for video in videos:
        vid = video['id']['videoId']
        details_url = f"https://www.googleapis.com/youtube/v3/videos?part=statistics&id={vid}&key={YOUTUBE_API_KEY}"
        details_response = requests.get(details_url)

        if details_response.status_code != 200:
            continue

        stats = details_response.json().get('items', [{}])[0].get('statistics', {})

        Video.objects.update_or_create(
            vid=vid,
            defaults={
                "url": f"https://www.youtube.com/watch?v={vid}",
                "title": video['snippet']['title'],
                "desc": video['snippet']['description'],
                "likes": int(stats.get('likeCount', 0)),
                "views": int(stats.get('viewCount', 0)),
                "pub_date": video['snippet']['publishedAt'],
                "thumb": video['snippet']['thumbnails']['high']['url']
            }
        )

    return {"message": "Videos fetched successfully"}


@shared_task
def example_task(x, y):
    return x + y  
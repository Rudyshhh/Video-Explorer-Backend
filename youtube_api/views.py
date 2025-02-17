from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from django.db.models import Q

from rest_framework import status
from .models import YouTubeVideo,Video

import requests




from .pagination import VideoPagination

from .models import Video
from .serializers import VideoSerializer
from .tasks import fetch_youtube_videos

class FetchVideosView(APIView):
    def post(self, request):
        query = request.data.get("query", "")
        if not query:
            return Response({"error": "Query required"}, status=status.HTTP_400_BAD_REQUEST)

        fetch_youtube_videos.delay(query)  # Run task asynchronously
        return Response({"message": "Fetching videos in the background"}, status=status.HTTP_202_ACCEPTED)

class ListVideosView(APIView):
    def get(self, request):
        videos = Video.objects.all().order_by("-pub_date")[:20]
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


YOUTUBE_API_KEY= "AIzaSyCCdxweLAQcCm7F72H8bQSHikYF_5SCQ3c"
class YouTubeTestView(APIView):
    def post(self, request):
        query = request.data.get('query', '')
        if not query:
            return Response({'error': 'Query parameter is missing'}, status=status.HTTP_400_BAD_REQUEST)

        url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&type=video&key={YOUTUBE_API_KEY}"
        response = requests.get(url)

        if response.status_code == 200:
            return Response(response.json(), status=status.HTTP_200_OK)
        else:
            return Response({'error': 'YouTube API request failed', 'details': response.text}, status=response.status_code)
        

class FilteredVideoListView(ListAPIView):
    serializer_class = VideoSerializer
    pagination_class = VideoPagination  

    def get_queryset(self):
        queryset = Video.objects.all()

        keyword = self.request.query_params.get('keyword', None)
        min_likes = self.request.query_params.get('min_likes', None)
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        ordering = self.request.query_params.get('ordering', None)

        if keyword:
            queryset = queryset.filter(
                Q(title__icontains=keyword) | Q(desc__icontains=keyword)
            )

        if min_likes:
            queryset = queryset.filter(likes__gte=min_likes)

        if start_date and end_date:
            queryset = queryset.filter(pub_date__range=[start_date, end_date])

        ordering_fields = {
            'relevance': ('-likes', '-views'),  # Sort by likes, then views
            'likes': '-likes',
            'published_date': '-pub_date',
            'views': '-views'
        }
        if ordering in ordering_fields:
            if isinstance(ordering_fields[ordering], tuple):
                queryset = queryset.order_by(*ordering_fields[ordering])
            else:
                queryset = queryset.order_by(ordering_fields[ordering])

        return queryset
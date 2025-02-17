

import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

YOUTUBE_API_KEY = "AIzaSyCCdxweLAQcCm7F72H8bQSHikYF_5SCQ3c"  

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



from django.urls import path,include
from .views import YouTubeTestView, FilteredVideoListView
from django.urls import path
from .views import FetchVideosView, ListVideosView

urlpatterns = [
    path('fetch-videos/', FetchVideosView.as_view(), name='fetch-videos'),
    path('list-videos/', ListVideosView.as_view(), name='list-videos'),
    path('test-youtube/', YouTubeTestView.as_view(), name='youtube-test'),
    path('filtered-videos/', FilteredVideoListView.as_view(), name='filtered-videos'),
]

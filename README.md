# Video Management API

This is a Django-based API for managing and filtering video data, fetching YouTube videos, and performing asynchronous background tasks with Celery. It allows users to fetch videos from YouTube, filter them by various parameters, and store them in a database for later use.

## Features

- **Fetch YouTube Videos**: Fetch videos from YouTube based on a search query and store the results in the database.
- **List Videos**: Retrieve a list of the latest videos stored in the database.
- **Filtered Video Search**: Filter videos based on keywords, likes, views, date range, and sorting options.
- **Asynchronous Processing with Celery**: Use Celery to fetch YouTube videos in the background, ensuring a non-blocking experience.
- **Test YouTube API**: Test fetching YouTube video data directly from the YouTube API.

## Technologies Used

- **Django**: Backend web framework.
- **Django REST Framework**: For building APIs and serializing data.
- **Celery**: For background tasks.
- **Redis**: Used as the message broker for Celery tasks.
- **YouTube API**: For fetching video data from YouTube.
- **PostgreSQL (or another database)**: For storing video metadata.

## Installation

### Prerequisites

1. Install **Redis** (used for Celery task queue):
   - Follow [Redis installation instructions](https://redis.io/download) for your operating system.

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

### Setting Up

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/video-management-api.git
   cd video-management-api
   ```

2. Set up the database (assuming you are using PostgreSQL):
   ```bash
   python manage.py migrate
   ```


3. Run Redis:
   ```bash
   redis-server
   ```

4. Start Celery worker:
   ```bash
   celery -A backend worker --loglevel=info --pool=solo
   ```

5. Start the Django development server:
   ```bash
   python manage.py runserver
   ```

6. Open your browser and visit `http://localhost:8000/api` to begin using the API.

## API Endpoints

### `POST /fetch-videos/`

Fetch YouTube videos based on the provided search query. This task runs asynchronously in the background.

#### Request Body:
```json
{
  "query": "search term"
}
```

#### Response:
```json
{
  "message": "Fetching videos in the background"
}
```

### `GET /list-videos/`

Get the latest 20 videos stored in the database.

#### Response:
```json
[
  {
    "id": 1,
    "title": "Video Title",
    "desc": "Video Description",
    "likes": 150,
    "views": 1200,
    "pub_date": "2023-02-10T12:00:00Z",
    "thumb": "https://example.com/thumbnail.jpg"
  }
]
```

### `POST /test-youtube/`

Fetch video data from the YouTube API for a specific search query.

#### Request Body:
```json
{
  "query": "search term"
}
```

#### Response:
```json
{
  "items": [
    {
      "snippet": {
        "title": "YouTube Video Title",
        "description": "Video Description",
        "publishedAt": "2023-02-10T12:00:00Z",
        "thumbnails": {
          "default": {
            "url": "https://example.com/thumbnail.jpg"
          }
        }
      }
    }
  ]
}
```

### `GET /filtered-videos/`

Get a filtered list of videos based on query parameters. You can filter by keyword, likes, date range, and ordering.

#### Query Parameters:
- `keyword`: Filter videos by title or description.
- `min_likes`: Filter videos with at least the specified number of likes.
- `start_date`: Filter videos published after this date (format: `YYYY-MM-DD`).
- `end_date`: Filter videos published before this date (format: `YYYY-MM-DD`).
- `ordering`: Order videos by field (`likes`, `published_date`, `views`, or `relevance`).

#### Example Request:
```http
GET /filtered-videos/?keyword=python&min_likes=1000&start_date=2023-01-01&end_date=2023-12-31&ordering=likes
```

#### Response:
```json
[
  {
    "id": 1,
    "title": "Filtered Video Title",
    "desc": "Video Description",
    "likes": 1200,
    "views": 15000,
    "pub_date": "2023-02-10T12:00:00Z",
    "thumb": "https://example.com/thumbnail.jpg"
  }
]
```

## Models

### `Video`
Represents a video in the system.

- **vid**: Unique video ID
- **url**: URL of the video
- **title**: Video title
- **desc**: Video description
- **likes**: Number of likes
- **views**: Number of views
- **pub_date**: Publication date
- **thumb**: Thumbnail URL

### `YouTubeVideo`
Represents a YouTube video fetched via the YouTube API.

- **title**: YouTube video title
- **description**: YouTube video description
- **vid**: YouTube video ID (unique)
- **published_at**: YouTube video publication date

## Celery Integration

### Background Task: `fetch_youtube_videos`

The `fetch_youtube_videos` task fetches YouTube videos asynchronously based on a search query, and stores relevant data in the `Video` model. It uses the YouTube Data API to get video details and statistics.

To run the task in the background, use Celery as the task queue:

```bash
celery -A backend worker --loglevel=info --pool=solo
```

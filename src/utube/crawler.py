from apiclient.discovery import build
from constellation import settings
from utube.utils import store_videos
from utube.models import VideoCategory

REGION_CODE = 'US'
MAX_DATA = 100
MAX_RESULT = 50
youtube = build(settings.YOUTUBE_API_SERVICE_NAME, settings.YOUTUBE_API_VERSION,
                developerKey=settings.DEVELOPER_KEY)


def get_video_categories():
    categories = youtube.videoCategories().list(
        part='id,snippet',
        regionCode='US',
    ).execute()
    result = []
    records = []
    for c in categories.get('items', []):
        id, name = c['id'], c['snippet']['title']
        result.append((id, name))
        records.append(VideoCategory(youtube_id=id, title=name))
    VideoCategory.objects.bulk_create(records)
    return result


def youtube_search():
    # Call the search.list method to retrieve results matching the specified
    # query term.
    categories = get_video_categories()
    for category in categories:
        id, name = category
        print "Search youtube for category {}".format(name)
        search_response = youtube.search().list(
            type='video',
            part="id",
            videoCategoryId=id,
            maxResults=MAX_RESULT,
        ).execute()
        yield search_response.get("items", [])
        token = search_response.get('nextPageToken', None)
        num = MAX_DATA - MAX_RESULT
        while token is not None and num > 0:
            search_response = youtube.search().list(
                type='video',
                part="id",
                maxResults=MAX_RESULT,
                videoCategoryId=id,
                pageToken=token
            ).execute()
            token = search_response.get('nextPageToken', None)
            num -= MAX_RESULT
            yield search_response.get("items", [])


def get_id_list():
    data = youtube_search()
    for d in data:
        ids = []
        for item in d:
            ids.append(item['id']['videoId'])
        yield ','.join(ids)


def get_video_detail():
    ids = get_id_list()
    for id in ids:
        response = youtube.videos().list(
            part='snippet,statistics',
            id=id,
            maxResults=MAX_RESULT
        ).execute()
        for item in response.get('items', []):
            yield item


def crawl_video():
    res = get_video_detail()
    store_videos(res)

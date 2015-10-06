from utube.models import Video


def store_videos(videos):
    def make_record(row):
        return Video(
            youtube_id=row.get('id'),
            title=row['snippet']['title'],
            thumbnail_url=row['snippet']['thumbnails']['default']['url'],
            channel_id=row['snippet']['channelId'],
            category_id=row['snippet']['categoryId'],
            view_count=row['statistics']['viewCount'],
            like_count=row['statistics']['likeCount'],
            dislike_count=row['statistics']['dislikeCount'],
            favorite_count=row['statistics']['favoriteCount'],
            comment_count=row['statistics']['commentCount']
        )
    records = map(make_record, videos)
    Video.objects.bulk_create(records)
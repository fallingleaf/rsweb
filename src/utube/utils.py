from utube.models import Video


def store_videos(videos):
    def make_record(row):
        return Video(
            youtube_id=row.get('id'),
            title=row['snippet']['title'],
            thumbnail_url=row['snippet']['thumbnails']['default']['url'],
            channel_id=row['snippet']['channelId'],
            category_id=row['snippet']['categoryId'],
            view_count=row['statistics'].get('viewCount', 0),
            like_count=row['statistics'].get('likeCount', 0),
            dislike_count=row['statistics'].get('dislikeCount', 0),
            favorite_count=row['statistics'].get('favoriteCount', 0),
            comment_count=row['statistics'].get('commentCount', 0)
        )

    records = map(make_record, videos)
    Video.objects.bulk_create(records)

from django.db import models
from oauth2client.django_orm import FlowField, CredentialsField
from jupiter.models import AuthUser
# Create your models here.

class FlowModel(models.Model):
    id = models.ForeignKey(AuthUser, primary_key=True)
    flow = FlowField()


class CredentialsModel(models.Model):
    id = models.ForeignKey(AuthUser, primary_key=True)
    credential = CredentialsField()


class VideoCategory(models.Model):
    youtube_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=256)
    
    
class Video(models.Model):
    youtube_id = models.CharField(max_length=128)
    title = models.TextField(blank=True)
    thumbnail_url = models.TextField(blank=True)
    channel_id = models.CharField(max_length=128, blank=True)
    category_id = models.IntegerField(blank=True, null=True)
    view_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    dislike_count = models.IntegerField(default=0)
    favorite_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    fetched_time = models.DateField(auto_now_add=True)

    def _get_video_url(self):
        return "http://www.youtube.com/watch?v=%s" % (self.youtube_id,)
    
    video_url = property(_get_video_url)


class UserVideo(models.Model):
    user = models.ForeignKey(AuthUser)
    video_id = models.CharField(max_length=128)
    is_like = models.BooleanField(default=False)
    is_favorite = models.BooleanField(default=False)

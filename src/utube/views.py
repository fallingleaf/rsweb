import os
import httplib2

from django.db.models import Count
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from constellation import settings
from utube.models import CredentialsModel, Video, UserVideo, VideoCategory
from utube.utils import store_videos
from utube.crawler import crawl_video
from jupiter.models import AuthUser
from jupiter.decorators import allow

from apiclient.discovery import build
from oauth2client import xsrfutil
from oauth2client.client import flow_from_clientsecrets
from oauth2client.django_orm import Storage

CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), '..', 'client_secret.json')

YOUTUBE_SCOPE = 'https://www.googleapis.com/auth/youtube'
REDIRECT_URI = 'http://localhost:8000/utube/callback'
MAX_RESULTS = 50

FLOW = flow_from_clientsecrets(CLIENT_SECRETS, 
        scope=YOUTUBE_SCOPE, 
        redirect_uri=REDIRECT_URI
        )
FLOW.params['access_type'] = 'offline'

def get_user_videos(service):
    response = service.channels().list(
        part='contentDetails',
        mine=True,
        maxResults=MAX_RESULTS
    ).execute()
    playlist_ids = []
    for channel in response.get('items', []):
        playlists = channel['contentDetails']['relatedPlaylists']
        if playlists:
            playlist_ids.extend(playlists.items())
    
    # Playlist name: likes, favorites, uploads, watchHistory, watchLater
    for (plname, plid) in playlist_ids:
        item_req = service.playlistItems().list(
            playlistId=plid,
            part='contentDetails',
            maxResults=50
        )
        while item_req:
            response = item_req.execute()
            for video in response.get('items', []):
                yield (video['contentDetails']['videoId'], plname)
            item_req = service.playlistItems().list_next(
                item_req, response
            )


def store_user_videos(user, videos):
    def make_record(inst):
        vid, plname = inst
        if plname == 'likes':
            return UserVideo(user=user, video_id=vid, is_like=True)
        if plname == 'favorites':
            return UserVideo(user=user, video_id=vid, is_favorite=True)
        return UserVideo(user=user, video_id=vid)
    
    records = map(make_record, videos)
    UserVideo.objects.bulk_create(records)
    
    
def update_user_infos(user, service):
    videos = get_user_videos(service)
    videos = [x for x in videos]
    store_user_videos(user, videos)
    
    ids = [x for (x, _) in videos]
    ids = list(set(ids))
    num = MAX_RESULTS
    partition = [ids[i*num : (i + 1)*num] for i in range(len(ids)/num + 1)]
    for p in partition:
        id_str = ','.join(p)
        if id_str:
            res = service.videos().list(
                part='snippet,statistics',
                id=id_str,
                maxResults=num
            ).execute()
            store_videos(res.get('items', []))
    
    
@login_required
def index(request):
    storage = Storage(CredentialsModel, 'id', request.user, 'credential')
    credential = storage.get()
    if credential is None or credential.invalid == True:
        FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY,
                                request.user)
        authorize_url = FLOW.step1_get_authorize_url()
        return redirect(authorize_url)
    else:
        user = AuthUser.objects.get(pk=request.user.id)
        video_count = user.uservideo_set.count()
        videos = Video.objects.raw(
            '''
            SELECT DISTINCT v.* FROM utube_video v LEFT JOIN utube_uservideo uv 
            ON uv.video_id = v.youtube_id 
            WHERE uv.user_id = %s
            ''', [user.id])
        if not video_count:
            http = httplib2.Http()
            http = credential.authorize(http)
            service = build('youtube', 'v3', http=http)
            update_user_infos(user, service)
        return render(request, 'utube/index.html', {'videos':videos})

@login_required
def callback(request):
    #if not xsrfutil.validate_token(settings.SECRET_KEY, request.GET['state'],
                                     #request.user):
        #return  HttpResponseBadRequest()
    credential = FLOW.step2_exchange(request.GET)
    print credential
    storage = Storage(CredentialsModel, 'id', request.user, 'credential')
    storage.put(credential)
    return redirect('/utube')

      
@login_required
def videos(request):
    total = Video.objects.count()
    categories = VideoCategory.objects.all()
    category_videos = Video.objects.values('category_id').annotate(videos=Count('category_id'))
    statistics = {}
    num_videos = []
    for cv in category_videos:
        statistics[cv['category_id']] = cv['videos']
    for ct in categories:
        num_videos.append((ct.title, statistics.get(ct.youtube_id, 0)))
    print num_videos
    if request.method == 'POST':
        Video.objects.all().delete()
        VideoCategory.objects.all().delete()
        crawl_video()
        return redirect('/utube/videos')
    return render(request, 'utube/videos.html', dict(total=total, 
        videos=num_videos))
        



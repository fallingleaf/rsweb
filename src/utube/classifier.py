from utube.models import Video, UserVideo
from django.db import connection
import numpy
from sklearn import tree
import random

def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
    

def discretize_data(d):
    r = []
    r.append(d[0])
    if d[1] >= 1000000:
        r.append(1)
    else:
        r.append(0)
    if d[2] >= 100000:
        r.append(1)
    else:
        r.append(0)
    if d[3] >= 100000:
        r.append(1)
    else:
        r.append(0)
    if d[4] >= 10000:
        r.append(1)
    else:
        r.append(0)
    if d[5] >= 10000:
        r.append(1)
    else:
        r.append(0)
    if d[6] is not None:
        r.append(d[6])
    else:
        r.append(r[4])
    return r
        

def build_classifier(user):
    data = []
    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT v.category_id, v.view_count, v.like_count, v.dislike_count,
             v.favorite_count, v.comment_count,
             CAST(uv.is_favorite AS INTEGER) AS favorite 
             FROM utube_video v LEFT JOIN utube_uservideo uv 
              ON v.youtube_id = uv.video_id WHERE uv.user_id = %s
        ''', [user.id])
        data = [list(x) for x in cursor.fetchall()]
    x = [d[:6] for d in data]
    y = [d[-1] for d in data]
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(x, y)
    return clf
    

def build_test_set():
    d = []
    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT v.youtube_id, v.title, v.thumbnail_url, v.category_id,
             v.view_count, v.like_count, v.dislike_count, v.favorite_count, v.comment_count  
             FROM utube_video v LEFT JOIN utube_uservideo uv 
             ON v.youtube_id = uv.video_id WHERE uv.is_favorite IS NULL
        ''', [])
        d = [x for x in cursor.fetchall()]
    src = dict([(hash(x[3:]), x[:3]) for x in d])
    data = [list(x[3:]) for x in d]
    return (src, data)


def predict(user):
    classifier = build_classifier(user)
    #print_tree(classifier)
    src, data = build_test_set()
    result = []
    target = 1
    for t in data[:50]:
        ps = classifier.predict(t)
        if ps[0] == target:
            idx = hash(tuple(t))
            result.append(src[idx])
    return result
    

    
    
        
    
    
    
    
    
    
    
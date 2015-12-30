from django.db import connection
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.neighbors import KNeighborsClassifier


def extract_data(uid):
    train = []
    test = []
    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT v.youtube_id, v.title, v.thumbnail_url 
             FROM utube_video v LEFT JOIN utube_uservideo uv 
             ON v.youtube_id = uv.video_id WHERE (uv.user_id != %s OR uv.user_id is NULL) AND v.title != ''
        ''', [uid])
        test = [x for x in cursor.fetchall()]

        cursor.execute('''
            SELECT v.title, uv.is_favorite 
             FROM utube_video v LEFT JOIN utube_uservideo uv 
             ON v.youtube_id = uv.video_id WHERE uv.user_id = %s AND v.title != '' 
        ''', [uid])
        train = [x for x in cursor.fetchall()]

    src = [x for x in test]
    test = [x[1] for x in test]
    y = [x[1] for x in train]
    train = [x[0] for x in train]
    return (train, y, src, test)


def tfidf_classify(user):
    train_set, y, src, test_set = extract_data(user.id)
    if not train_set:
        return []
    # Analyse using tf-idf
    # vector = TfidfVectorizer(sublinear_tf=True, max_df=0.5)
    vector = HashingVectorizer(n_features=1000, non_negative=True, stop_words='english')
    # List of topic extracted from text
    # feature_names = vector.get_feature_names()
    # print feature_names
    xtrain = vector.transform(train_set)
    xtest = vector.transform(test_set)

    # Select sample using chi-square
    ch2 = SelectKBest(chi2)
    xtrain = ch2.fit_transform(xtrain, y)
    xtest = ch2.transform(xtest)

    # Predict testing set
    # classifier = DecisionTreeClassifier()
    classifier = KNeighborsClassifier(n_neighbors=4)
    classifier = classifier.fit(xtrain, y)
    result = classifier.predict(xtest)
    final = []
    for i in xrange(len(result)):
        if result[i]:
            final.append(src[i])
    print len(final)
    return final

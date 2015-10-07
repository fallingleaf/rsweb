#Web Portfolio and Demo#

##Deloyment instruction##

*Setup virtual environment*
- Install virtualenv `pip install virtualenv`
- Set project environment `virtualenv .`
- Activate python env `. .env/bin/activate`
- Install necessary packages `pip install -r requirement.txt`

*Configure project*
- Change directory to `src`
- Copy sample settings `cp settings.py.example settings.py`
- Update database connection dbname, username, password in setting file
- Update Youtube API key to your key

*Migration*
- Run database migration `python manage.py migrate`

*Add admin account*
- `python manage.py createsuperuer` and follow instruction to add admin user
- Using admin interface, user can add one or more accounts for testing purpose `localhost:8000/admin`

*Run server*
- `python manange.py runserver`

*Craw youtube data*
- Navigate to website (on your localhost): `localhost:8000/utube/videos`

*Test user's video page*
- `localhost:8000/utube` (this page requires login and links account to youtube)

*Notes:*
- Server uses default credentials from **client_secret.json**, you can generate your own credentials using google developer console.
- As you might use different domain, config your Google oauth to use different callback uri, and YOUTUBE_REDIRECT_URI in setting file
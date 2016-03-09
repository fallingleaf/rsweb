#Web Portfolio and Demo#

##Deloyment instruction##

*Requirements:*
- Python 2.7.11
- Django 1.8.3
- Django Rest Framework 3.1.3
- PostgreSQL 9.4

*Setup virtual environment*
- Install virtualenv `pip install virtualenv`
- Set project environment `virtualenv .`
- Activate python env `. .env/bin/activate`
- Install necessary packages `pip install -r requirement.txt`

*Configure project*
- Change directory to `cd src`
- Copy sample settings `cp settings.py.example settings.py`
- Update database connection dbname, username, password in setting file

*Migration*
- Run database migration `python manage.py migrate`

*Run server*
- `python manange.py runserver` or `python manage.py runserver [port-number]`
- Open browser and navigate to: http://localhost:8000/. The website will display portfolio page.

*Run tests*
- `python manage.py test`

*API List*
- Submit event:     http://localhost:8000/nationbuilder/events
- List event:       http://localhost:8000/nationbuilder/events?from=2016-03-09T00:00:00Z&to=2016-03-10T00:00:00Z
- Clear data:       http://localhost:8000/nationbuilder/events/clear
- Event summary:    http://localhost:8000/nationbuilder/events/summary?from=2016-03-09T00:00:00Z&to=2016-03-10T00:00:00Z&by=hour

*Notes:*
- To test against server API using `curl`for example: `curl ­H  "Content­Type: application/json" ­X  POST ­d ' {"date": "2016-03­-09T09:00:00Z", "user": "Doc", "type": "enter"} '  http://localhost:8000/nationbuilder/events`
- Sample server: http://tamhoangnguyen.me/
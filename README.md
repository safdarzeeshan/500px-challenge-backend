#500px challenge API

This API was created in Django Rest to support the following methods

- Get Authorization URL to login with 500px.com
- Get oauth token and secret form 500px.com
- Complete login/registration to app with 500px.com credentials
- Get popular photos from 500px.com
- Get specific photo's details
- Like a picture from 500px.com
- Unlike a picture from 500px.com

#Setup

To install dependencies `pip install -r requirements.txt`

In `settings.py` change your database settings, consumer key & consumer secret

To create the database `./manage.py migrate`

To run locally `./manage.py runserver`

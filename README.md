#500px challenge API

This API was created in Djangoto support the following methods

- Complete OAuth login with 500px.com
- Create user with social auth 500px.com
- Get popular photos
- Like a picture from 500px.com
- Unlike a picture from 500px.com

#Setup

To install dependencies `pip install -r requirements.txt`

In `settings.py` change your database settings, consumer key & consumer secret

To create the database `./manage.py migrate`

To run locally `./manage.py runserver`

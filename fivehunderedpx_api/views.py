from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
import requests
from django.http import JsonResponse
import json
from requests_oauthlib import OAuth1Session, OAuth1
from fivehunderedpx_api.models import *
from fivehunderedpx_api.serializers import *
from allauth.socialaccount.providers.fivehundredpx.views import FiveHundredPxOAuthAdapter
from rest_auth.views import LoginView
from django.contrib.auth.models import AnonymousUser


class FiveHundredPxLogin(LoginView):
    serializer_class = FiveHundredPxLoginSerializer
    adapter_class = FiveHundredPxOAuthAdapter


class PopularPhotosList(APIView):

    consumer_key = 'YI4wh0gAdmryhV27jqUBYtIAUdv5qvDrA4qyf5AK'
    consumer_secret = 'YFze8NX1IlfwQzLJUc9I54QsO2dniWEpWFk2FxCk'
    base_url = 'https://api.500px.com/v1/'

    def get(self, request):

        # Make a request with consumer key
        user = self.request.user
        # print user.socialaccount

        if user == AnonymousUser():
            response = requests.get(
                self.base_url + 'photos/',
                params = {'feature': 'popular', 'image_size':'3,5', 'consumer_key': self.consumer_key})

        # Make a request with User Auth token
        else:
            oauth = SocialToken.objects.get(account__user=user, account__provider='500px')
            auth = OAuth1(self.consumer_key, self.consumer_secret, oauth.token, oauth.token_secret)
            response = requests.get(
                self.base_url + 'photos/',
                auth=auth,
                params = {'feature': 'popular', 'image_size': '3,5', 'include_states': 'voted'})

        return JsonResponse(json.loads(response.content))


class PhotoDetail(APIView):

    permission_classes = IsAuthenticated,
    consumer_key = 'YI4wh0gAdmryhV27jqUBYtIAUdv5qvDrA4qyf5AK',
    base_url = 'https://api.500px.com/v1/'

    def get(self, request):

        photo_id = request.GET.get('photoId')
        response = requests.get(
            self.base_url + 'photos/' + photo_id,
            params =  {'consumer_key': self.consumer_key})

        return JsonResponse(json.loads(response.content))


class LikePhoto(APIView):

    consumer_key = 'YI4wh0gAdmryhV27jqUBYtIAUdv5qvDrA4qyf5AK'
    consumer_secret = 'YFze8NX1IlfwQzLJUc9I54QsO2dniWEpWFk2FxCk'
    base_url = 'https://api.500px.com/v1/'

    def get(self, request):

        user = self.request.user
        oauth = SocialToken.objects.get(account__user=user, account__provider='500px')
        auth = OAuth1(self.consumer_key, self.consumer_secret, oauth.token, oauth.token_secret)

        photo_id = request.GET.get('photoId')
        response = requests.post(
            self.base_url + 'photos/' + photo_id + '/vote',
            auth=auth,
            params={'vote': '1'})

        return JsonResponse(json.loads(response.content))


class RequestToken(APIView):

    def get(self, request):

        consumer_key = 'YI4wh0gAdmryhV27jqUBYtIAUdv5qvDrA4qyf5AK'
        consumer_secret = 'YFze8NX1IlfwQzLJUc9I54QsO2dniWEpWFk2FxCk'

        request_token_url = 'https://api.500px.com/v1/oauth/request_token'
        authorization_base_url = 'https://api.500px.com/v1/oauth/authorize'
        access_token_url = 'https://api.500px.com/v1/oauth/access_token'

        # Fetch a request token
        fivehundredpx = OAuth1Session(consumer_key, client_secret=consumer_secret, callback_uri='http://127.0.0.1:9000/redirect')
        fetch_response = fivehundredpx.fetch_request_token(request_token_url)

        resource_owner_key = fetch_response.get('oauth_token')
        resource_owner_secret = fetch_response.get('oauth_token_secret')
        OauthTokenSecret.objects.create(oauth_token=resource_owner_key, oauth_token_secret=resource_owner_secret)

        # Redirect user to 500px for authorization
        authorization_url = fivehundredpx.authorization_url(authorization_base_url, callback_uri='http://127.0.0.1:9000/redirect')

        return JsonResponse({'authorization_url': authorization_url})


class AccessToken(APIView):

    def get(self, request):

        consumer_key = 'YI4wh0gAdmryhV27jqUBYtIAUdv5qvDrA4qyf5AK'
        consumer_secret = 'YFze8NX1IlfwQzLJUc9I54QsO2dniWEpWFk2FxCk'
        access_token_url = 'https://api.500px.com/v1/oauth/access_token'

        oauth_verifier = request.GET.get('oauth_verifier')
        oauth_token = request.GET.get('oauth_token')

        print oauth_verifier
        print oauth_token
        resource_owner_secret = OauthTokenSecret.objects.get(oauth_token=oauth_token).oauth_token_secret

        print resource_owner_secret
        oauth = OAuth1Session(consumer_key,
                          client_secret=consumer_secret,
                          resource_owner_key=oauth_token,
                          resource_owner_secret=resource_owner_secret,
                          verifier=oauth_verifier)

        oauth_tokens = oauth.fetch_access_token(access_token_url)

        print oauth_tokens

        return JsonResponse({'access_token': oauth_tokens['oauth_token'], 'token_secret':oauth_tokens['oauth_token_secret']})


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
from fivehunderedpx_challenge_api.settings import *


class FiveHundredPxLogin(LoginView):
    serializer_class = FiveHundredPxLoginSerializer
    adapter_class = FiveHundredPxOAuthAdapter


class PopularPhotosList(APIView):

    def get(self, request):

        user = self.request.user

        # Make a request with consumer key
        if user == AnonymousUser():
            response = requests.get(
                settings.BASE_URL + 'photos/',
                params = {'feature': 'popular', 'image_size':'4,5', 'consumer_key': settings.CONSUMER_KEY})

        # Make a request with User Auth token
        else:
            oauth = SocialToken.objects.get(account__user=user, account__provider='500px')
            auth = OAuth1(settings.CONSUMER_KEY, settings.CONSUMER_SECRET, oauth.token, oauth.token_secret)
            response = requests.get(
                settings.BASE_URL + 'photos/',
                auth=auth,
                params = {'feature': 'popular', 'image_size': '4,5', 'include_states': 'voted'})

        return JsonResponse(json.loads(response.content))


class PhotoDetail(APIView):

    permission_classes = IsAuthenticated

    def get(self, request):

        photo_id = request.GET.get('photoId')
        response = requests.get(
            settings.BASE_URL + 'photos/' + photo_id,
            params = {'consumer_key': settings.CONSUMER_KEY})

        return JsonResponse(json.loads(response.content))


class LikePhoto(APIView):

    def get(self, request):

        user = self.request.user
        oauth = SocialToken.objects.get(account__user=user, account__provider='500px')
        auth = OAuth1(settings.CONSUMER_KEY, settings.CONSUMER_SECRET, oauth.token, oauth.token_secret)

        photo_id = request.GET.get('photoId')
        response = requests.post(
            settings.BASE_URL + 'photos/' + photo_id + '/vote',
            auth=auth,
            params={'vote': '1'})

        return JsonResponse(json.loads(response.content))


class UnlikePhoto(APIView):

    def get(self, request):

        user = self.request.user
        oauth = SocialToken.objects.get(account__user=user, account__provider='500px')
        auth = OAuth1(settings.CONSUMER_KEY, settings.CONSUMER_SECRET, oauth.token, oauth.token_secret)

        photo_id = request.GET.get('photoId')
        response = requests.delete(
            settings.BASE_URL + 'photos/' + photo_id + '/vote',
            auth=auth)

        return JsonResponse(json.loads(response.content))


class RequestToken(APIView):

    def get(self, request):

        request_token_url = 'https://api.500px.com/v1/oauth/request_token'
        authorization_base_url = 'https://api.500px.com/v1/oauth/authorize'

        # Fetch a request token
        fivehundredpx = OAuth1Session(settings.CONSUMER_KEY, client_secret=settings.CONSUMER_SECRET, callback_uri='http://127.0.0.1:9000/redirect')
        fetch_response = fivehundredpx.fetch_request_token(request_token_url)

        resource_owner_key = fetch_response.get('oauth_token')
        resource_owner_secret = fetch_response.get('oauth_token_secret')
        OauthTokenSecret.objects.create(oauth_token=resource_owner_key, oauth_token_secret=resource_owner_secret)

        # Redirect user to 500px for authorization
        authorization_url = fivehundredpx.authorization_url(authorization_base_url, callback_uri='http://127.0.0.1:9000/redirect')

        return JsonResponse({'authorization_url': authorization_url})


class AccessToken(APIView):

    def get(self, request):

        access_token_url = 'https://api.500px.com/v1/oauth/access_token'

        oauth_verifier = request.GET.get('oauth_verifier')
        oauth_token = request.GET.get('oauth_token')

        resource_owner_secret = OauthTokenSecret.objects.get(oauth_token=oauth_token).oauth_token_secret

        oauth = OAuth1Session(settings.CONSUMER_KEY,
                          client_secret=settings.CONSUMER_SECRET,
                          resource_owner_key=oauth_token,
                          resource_owner_secret=resource_owner_secret,
                          verifier=oauth_verifier)

        oauth_tokens = oauth.fetch_access_token(access_token_url)

        return JsonResponse({'access_token': oauth_tokens['oauth_token'], 'token_secret':oauth_tokens['oauth_token_secret']})


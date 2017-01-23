from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from django.http import JsonResponse
import json



class PopularPhotosList(APIView):

    consumer_key = 'YI4wh0gAdmryhV27jqUBYtIAUdv5qvDrA4qyf5AK'
    base_url = 'https://api.500px.com/v1/'

    def get(self, request):
        response = requests.get(
            self.base_url + 'photos/',
            params =  {'feature': 'popular', 'consumer_key': self.consumer_key})

        return JsonResponse(json.loads(response.content))


class PhotoDetail(APIView):

    consumer_key = 'YI4wh0gAdmryhV27jqUBYtIAUdv5qvDrA4qyf5AK'
    base_url = 'https://api.500px.com/v1/'

    def get(self, request):

        photo_id = request.GET.get('photoId')
        response = requests.get(
            self.base_url + 'photos/' + photo_id,
            params =  {'consumer_key': self.consumer_key})

        return JsonResponse(json.loads(response.content))
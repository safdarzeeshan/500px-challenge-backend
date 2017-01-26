from django.conf.urls import url
from django.contrib import admin
from fivehunderedpx_api.views import *
from django.conf.urls import include, url
from django.views.generic.base import TemplateView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^api/rest-auth/', include('rest_auth.urls')),
    url(r'^account-confirm-email/(?P<key>[-:\w]+)/$', TemplateView.as_view(), name='account_confirm_email'),
    # url(r'^api/rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^api/rest-auth/fivehundredpx/$', FiveHundredPxLogin.as_view(), name='FiveHundredPxLogin'),
    url(r'^api/popularphotos/', PopularPhotosList.as_view(), name="PopularPhotosList"),
    url(r'^api/photodetail$', PhotoDetail.as_view(), name="PhotoDetail"),
    url(r'^api/likephoto$', LikePhoto.as_view(), name="LikePhoto"),
    url(r'^api/unlikephoto$', UnlikePhoto.as_view(), name="LikePhoto"),
    url(r'^api/requesttoken/', RequestToken.as_view(), name="RequestToken"),
    url(r'^api/accesstoken$', AccessToken.as_view(), name="AccessToken"),
]

from django.conf.urls import url
from django.contrib import admin
from fivehunderedpx_api.views import *
from django.conf.urls import include, url

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/rest-auth/', include('rest_auth.urls')),
    # url(r'^api/rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^api/rest-auth/fivehundredpx/$', FiveHundredPxLogin.as_view(), name='FiveHundredPxLogin'),
    url(r'^api/popularphotos/', PopularPhotosList.as_view(), name="PopularPhotosList"),
    url(r'^api/photodetail$', PhotoDetail.as_view(), name="PhotoDetail"),
    url(r'^api/likephoto$', LikePhoto.as_view(), name="LikePhoto"),
    url(r'^api/requesttoken/', RequestToken.as_view(), name="RequestToken"),
    url(r'^api/accesstoken$', AccessToken.as_view(), name="AccessToken"),
]

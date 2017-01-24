from __future__ import unicode_literals
from django.db import models

class OauthTokenSecret(models.Model):

    oauth_token = models.CharField(max_length=500, blank=True)
    oauth_token_secret = models.CharField(max_length=500, blank=True)

    def __unicode__(self):
        return (self.oauth_token)
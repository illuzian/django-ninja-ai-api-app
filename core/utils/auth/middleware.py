import logging
from datetime import datetime, timedelta, timezone

import pendulum
import requests
from allauth.socialaccount.models import SocialToken
from django.conf import settings
from . import token as token_utils

MS_AUTH_CONFIG = settings.SOCIALACCOUNT_PROVIDERS['microsoft']['APPS'][0]


class RefreshTokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    # @staticmethod
    # def refresh_token(token):
    #     form_data = {
    #         "client_id": MS_AUTH_CONFIG['client_id'],
    #         "client_secret": MS_AUTH_CONFIG['secret'],
    #         'grant_type': 'refresh_token',
    #         'refresh_token': token.token_secret
    #     }
    #
    #     r = requests.post(
    #         f'https://login.microsoftonline.com/'
    #         f"{MS_AUTH_CONFIG['settings']['tenant']}/oauth2/v2.0/token", data=form_data)
    #     # print(r.json())
    #     return r.json()

    def __call__(self, request):
        if request.user.is_authenticated:
            logging.debug('user authenticated')
            token_manager = token_utils.UserTokenManager(request=request)
            logging.debug(token_manager.token)

            # token_utils.check_token_from_request(request)
            #
            # current_token = SocialToken.objects.get(account__user=request.user)
            # current_token.refresh_from_db()
            #
            # token_expires_at = pendulum.instance(current_token.expires_at)
            #
            # time_now = pendulum.now(tz=settings.TIME_ZONE)
            #
            # if token_expires_at < time_now:
            #     logging.info('token expired')
            #     new_token = self.refresh_token(current_token)
            #     new_expiry = datetime.utcnow() + timedelta(seconds=new_token['expires_in'] - 120)
            #
            #     current_token.expires_at = new_expiry.replace(tzinfo=timezone.utc)
            #     current_token.token = new_token['access_token']
            #     current_token.token_secret = new_token['refresh_token']
            #     current_token.save()
            #
            # else:
            #     logging.info('token valid')

        response = self.get_response(request)

        return response

import logging

import pendulum
import requests
from allauth.socialaccount.models import SocialToken
from django.conf import settings

MS_AUTH_CONFIG = settings.SOCIALACCOUNT_PROVIDERS['microsoft']['APPS'][0]


def refresh_token(token):
    form_data = {
        "client_id": MS_AUTH_CONFIG['client_id'],
        "client_secret": MS_AUTH_CONFIG['secret'],
        'grant_type': 'refresh_token',
        'refresh_token': token.token_secret
    }

    r = requests.post(
        f'https://login.microsoftonline.com/'
        f"{MS_AUTH_CONFIG['settings']['tenant']}/oauth2/v2.0/token", data=form_data)
    # print(r.json())
    return r.json()


def check_token(current_token):
    current_token.refresh_from_db()

    token_expires_at = pendulum.instance(current_token.expires_at)

    time_now = pendulum.now(tz=settings.TIME_ZONE)

    if token_expires_at < time_now:
        logging.debug('token expired')
        new_token = refresh_token(current_token)
        new_expiry = pendulum.now().add(seconds=new_token['expires_in'] - 120)

        current_token.expires_at = new_expiry
        current_token.token = new_token['access_token']
        current_token.token_secret = new_token['refresh_token']
        current_token.save()

    else:
        logging.debug('token valid')


def get_token_for_user(user):
    return SocialToken.objects.get(account__user=user)


def check_token_from_request(request):
    if not request.user.is_authenticated:
        logging.error('user not authenticated')
        return None
    current_token = SocialToken.objects.get(account__user=request.user)
    check_token(current_token)
    # scopes = ' '.join(settings.SOCIALACCOUNT_PROVIDERS['microsoft']['SCOPE'])
    # token_expires_at = pendulum.instance(current_token.expires_at)
    # time_now = pendulum.now(tz=settings.TIME_ZONE)
    #
    #
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


class UserTokenManager:
    def __init__(self, db_token=None, user=None, request=None):
        logging.debug('Instantiating UserToken')

        if not any([db_token, user, request]):
            raise ValueError('Either db_token, user or request must be provided')

        self._db_token = db_token

        if db_token is None and user is not None:
            logging.debug('Setting db_token from user')
            self.set_token_from_user(user)

        elif db_token is None and request is not None:
            logging.debug('Setting db_token from request')
            self.set_token_from_request(request)

        self.check_token()

    @property
    def token(self):
        self.check_token()
        scopes = ' '.join(settings.SOCIALACCOUNT_PROVIDERS['microsoft']['SCOPE'])
        return {
                'token_type': 'Bearer',
                'scope': scopes,
                'expires_in': 5252, 'ext_expires_in': 5252, 'access_token': self._db_token.token,
                'refresh_token': self._db_token.token_secret
            }

    def set_token_from_user(self, user):
        self._db_token = SocialToken.objects.get(account__user=user)

    def set_token_from_request(self, request):
        if not request.user.is_authenticated:
            logging.error('user not authenticated')
            return None
        current_token = SocialToken.objects.get(account__user=request.user)
        self._db_token = current_token

    def refresh_token(self):
        form_data = {
            "client_id": MS_AUTH_CONFIG['client_id'],
            "client_secret": MS_AUTH_CONFIG['secret'],
            'grant_type': 'refresh_token',
            'refresh_token': self._db_token.token_secret
        }

        r = requests.post(
            f'https://login.microsoftonline.com/'
            f"{MS_AUTH_CONFIG['settings']['tenant']}/oauth2/v2.0/token", data=form_data)

        new_token = r.json()
        new_expiry = pendulum.now().add(seconds=new_token['expires_in'] - 120)

        self._db_token.expires_at = new_expiry
        self._db_token.token = new_token['access_token']
        self._db_token.token_secret = new_token['refresh_token']
        self._db_token.save()

    def check_token(self):
        token_expires_at = pendulum.instance(self._db_token.expires_at)

        time_now = pendulum.now(tz=settings.TIME_ZONE)

        if token_expires_at < time_now:
            logging.debug('token expired')
            self.refresh_token()

        else:
            logging.debug('token valid')

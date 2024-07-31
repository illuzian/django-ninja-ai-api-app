from O365.utils.token import BaseTokenBackend, Token
from allauth.socialaccount.models import SocialToken
from django.conf import settings


class AppTokenBackend(BaseTokenBackend):
    def __init__(self, request):
        super().__init__()
        current_token = SocialToken.objects.get(account__user=request.user)
        scopes = ' '.join(settings.SOCIALACCOUNT_PROVIDERS['microsoft']['SCOPE'])

        if request.user.is_authenticated:
            self.token = {
                'token_type': 'Bearer',
                'scope': scopes,
                'expires_in': 5252, 'ext_expires_in': 5252, 'access_token': current_token.token,
                'refresh_token': current_token.token_secret
            }

    def load_token(self):
        return self.token

    def get_token(self):
        return self.token

    def save_token(self, token: Token):
        raise NotImplementedError

    def delete_token(self):
        raise NotImplementedError

    def check_token(self):
        return True

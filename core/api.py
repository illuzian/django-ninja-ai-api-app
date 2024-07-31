import requests
from allauth.socialaccount.models import SocialToken
from ninja import NinjaAPI
from ninja.security import django_auth

from testing import ask_email
from ai.core.transformers import transform_document

api = NinjaAPI()


@api.get("/get_mail", auth=django_auth)
def get_mail(request):
    token = SocialToken.objects.get(account__user=request.auth)

    # refreshed_token = refresh_token(token)

    headers = {'Authorization': f'Bearer {token.token}'}

    r = requests.get('https://graph.microsoft.com/v1.0/me/messages', headers=headers)
    print(r.json())

    transformed = transform_document(r.json()['value'][0]['body']['content'])
    return ask_email.ask_email(transformed)
    # return r.json()['value'][0]['body']
    # return transformed


@api.get("/hello", auth=django_auth)
def hello(request, name: str):
    token = SocialToken.objects.get(account__user=request.auth)

    headers = {'Authorization': f'Bearer {token.token}'}

    return f"{name}"

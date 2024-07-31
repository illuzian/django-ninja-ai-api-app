import logging

import O365
from django.conf import settings
from django.shortcuts import render

from core.utils.auth.o365 import AppTokenBackend


# Create your views here.
def home_view(request):
    if request.user.is_authenticated:
        from langchain_community.tools.office365.utils import authenticate
        import langchain_community
        token_backend = AppTokenBackend(request)

        account = O365.Account(
            (settings.SOCIALACCOUNT_PROVIDERS['microsoft']['APPS'][0]['client_id'],
             settings.SOCIALACCOUNT_PROVIDERS['microsoft']['APPS'][0]['secret']),
            token_backend=token_backend)
        langchain_community.tools.office365.utils.authenticate = account

    return render(request, 'main/home.html')

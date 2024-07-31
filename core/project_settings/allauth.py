import os

SOCIALACCOUNT_PROVIDERS = {
    "microsoft": {
        'SCOPE': [
            'profile',
            'email',
            'openid',
            'User.Read',
            "User.Read.All",
            "Mail.Read",
            "Mail.ReadWrite",
            "Calendars.ReadWrite",
            "MailboxSettings.ReadWrite",
            "Mail.Send",
            "offline_access"

        ],
        "APPS": [
            {
                "client_id": os.getenv('MS_CLIENT_ID'),
                "secret": os.getenv('MS_CLIENT_SECRET'),
                "settings": {
                    "tenant": os.getenv('MS_TENANT_ID'),
                    # Optional: override URLs (use base URLs without path)
                    "login_url": "https://login.microsoftonline.com",
                    "graph_url": "https://graph.microsoft.com",
                }
            }
        ]
    }
}

SOCIALACCOUNT_ONLY = True
ACCOUNT_EMAIL_VERIFICATION = 'none'
SOCIALACCOUNT_STORE_TOKENS = True
ACCOUNT_ADAPTER = 'core.utils.auth.allauth.ProjectAccountAdapter'

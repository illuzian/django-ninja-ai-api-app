from django.urls import path
from .views import home_view

app_name = 'main'

urlpatterns = [
    path(r'', home_view, name='home'),
]
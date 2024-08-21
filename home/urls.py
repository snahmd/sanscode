from django.urls import path
from blogpage.views import SubscribeView

urlpatterns = [
    path('subscribe/', SubscribeView.as_view(), name='subscribe'),
]
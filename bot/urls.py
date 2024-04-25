from bot import views
from django.urls import path

urlpatterns = [
    path(
        'status/',
        views.BotStatusAPIView.as_view(),
        name='ai'
    )
]

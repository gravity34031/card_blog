from .views import PhotoJSONListView
from django.urls import path, include

urlpatterns = [
    path('photolist/',
        PhotoJSONListView.as_view(),
        name='photologue_custom-photo-json-list'),
]
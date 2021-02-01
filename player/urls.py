from django.urls import path

from player import views

urlpatterns = [
    path('', views.index, name='home'),
    path('browse/<int:sid>/', views.browse, name='browse'),
    path('radio/', views.radio, name='radio'),
    path('albums/<int:sid>/', views.albums, name='albums'),
    path('albums/songs/<int:sid>/<album_id>', views.albumInfo, name='albums_details'),
    path('artists/<int:sid>/', views.artists, name='artists'),
    path('artists/songs/<int:sid>/<artist_id>', views.artistInfo, name='artists-details'),
    path('songs/<int:sid>', views.songs, name='songs'),
    path('search/<int:sid>/', views.search, name='search'),
]
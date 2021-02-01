import random

from django.db.models import Q
from django.shortcuts import render, redirect

# Create your views here.
from player.models import Artist, Album, Song, Browsepage


def find_song(song_id):
    song = Song.objects.filter(pk=song_id)

    if not song:
        return False
    else:
        song = song.get()

    song_ids = Song.objects.values_list('id', flat=True)

    sid_index = list(song_ids).index(song_id)

    if sid_index == 0:
        prev_id = '-1'
        next_id = str(song_ids[sid_index + 1])

    elif sid_index == len(song_ids) - 1:
        prev_id = str(song_ids[sid_index - 1])
        next_id = '-1'

    else:
        prev_id = str(song_ids[sid_index - 1])
        next_id = str(song_ids[sid_index + 1])

    return song, prev_id, next_id


def random_song_id():
    song_ids = Song.objects.values_list('id', flat=True)
    return random.choice(list(song_ids))


def index(request):
    return redirect('browse', sid=random_song_id())


def browse(request, sid):
    data = Browsepage.objects.all()

    if find_song(sid):
        song, prev_id, next_id = find_song(sid)

        song = Song.objects.filter(pk=sid)

        if not song:
            return redirect('browse', sid=random_song_id())
        else:
            song = song.get()

    else:
        return redirect('browse', sid=random_song_id())

    context = {'data': data, 'song': song, 'pid': prev_id, 'nid': next_id}
    return render(request, 'player/index.html', context)


def radio(request):
    context = {}
    return render(request, 'player/radio.html', context)


def songs(request, sid):
    all_songs = Song.objects.all()

    # Getting current song data
    if find_song(sid):
        song, prev_id, next_id = find_song(sid)
    else:
        song, prev_id, next_id = find_song(random_song_id())

    context = {'all_songs': all_songs, 'song': song, 'pid': prev_id, 'nid': next_id}
    return render(request, 'player/songs.html', context)


def albums(request, sid):
    all_albums = Album.objects.all()

    # Getting current song data
    if find_song(sid):
        song, prev_id, next_id = find_song(sid)
    else:
        song, prev_id, next_id = find_song(random_song_id())

    context = {'all_albums': all_albums, 'song': song, 'pid': prev_id, 'nid': next_id}
    return render(request, 'player/albums.html', context)


def artists(request, sid):
    all_artists = Artist.objects.all()

    # Getting current song data
    if find_song(sid):
        song, prev_id, next_id = find_song(sid)
    else:
        song, prev_id, next_id = find_song(random_song_id())

    context = {'all_artists': all_artists, 'song': song, 'pid': prev_id, 'nid': next_id}
    return render(request, 'player/artists.html', context)


def artistInfo(request, artist_id, sid):
    artist = Artist.objects.get(pk=artist_id)
    artist_songs = Song.objects.filter(artist_name=artist)

    # Getting current song data
    if find_song(sid):
        song, prev_id, next_id = find_song(sid)
    else:
        song, prev_id, next_id = find_song(random_song_id())

    context = {'artist': artist, 'artist_songs': artist_songs, 'song': song, 'pid': prev_id, 'nid': next_id}

    return render(request, 'player/artistInfo.html', context)


def albumInfo(request, sid, album_id):
    album = Album.objects.get(pk=album_id)
    album_songs = Song.objects.filter(album_Name=album)

    # Getting current song data
    if find_song(sid):
        song, prev_id, next_id = find_song(sid)
    else:
        song, prev_id, next_id = find_song(random_song_id())

    context = {'album': album, 'album_songs': album_songs, 'song': song, 'pid': prev_id, 'nid': next_id}
    return render(request, 'player/albumInfo.html', context)


def search(request, sid):
    if request.method == 'GET':
        if 'search' in request.GET.keys():
            keyword = request.GET['search']

            song_data = Song.objects.filter(
                Q(song_name__icontains=keyword) |
                Q(artist_name__artistName__icontains=keyword) |
                Q(album_Name__albumName__icontains=keyword)
            )

            # Getting current song data
            if find_song(sid):
                song, prev_id, next_id = find_song(sid)
            else:
                song, prev_id, next_id = find_song(random_song_id())

            return render(request, 'player/search.html',
                          {'song_data': song_data, 'song': song, 'pid': prev_id, 'nid': next_id})

        else:

            # Getting current song data
            if find_song(sid):
                song, prev_id, next_id = find_song(sid)
            else:
                song, prev_id, next_id = find_song(random_song_id())

            return render(request, 'player/search.html',
                          {'song': song, 'pid': prev_id, 'nid': next_id})

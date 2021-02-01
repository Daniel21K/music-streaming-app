from django.db import models

# Create your models here.


class Artist(models.Model):
    artistName = models.CharField(max_length=255)
    image = models.ImageField(upload_to='media/images')
    briefBio = models.TextField()

    def __str__(self):
        return self.artistName


class Album(models.Model):
    albumName = models.CharField(max_length=255)
    artWork = models.ImageField(upload_to='media/images')
    artist_name = models.ForeignKey(Artist, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=255)
    number_of_songs = models.IntegerField()
    album_desc = models.TextField(max_length=150, default="Popular Album!")

    def __str__(self):
        return self.albumName


class Song(models.Model):
    song_name = models.CharField(max_length=255)
    art_Work = models.ImageField(upload_to='media/images')
    song_file = models.FileField(upload_to='media/songs')
    artist_name = models.ForeignKey(Artist, on_delete=models.CASCADE)
    album_Name = models.ForeignKey(Album, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.song_name


class Browsepage(models.Model):
    albums = models.ForeignKey(Album, on_delete=models.CASCADE)
    artists = models.ForeignKey(Artist, on_delete=models.CASCADE, default="")
    songs = models.ForeignKey(Song, on_delete=models.CASCADE, default="")
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)


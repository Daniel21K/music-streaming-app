# Generated by Django 3.1.4 on 2021-01-25 10:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0002_remove_song_song_length'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='album_Name',
            field=models.ForeignKey(default='Single', on_delete=django.db.models.deletion.CASCADE, to='player.album'),
        ),
    ]

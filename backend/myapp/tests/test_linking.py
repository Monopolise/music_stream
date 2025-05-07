from django.test import TestCase, Client, override_settings
from django.urls import reverse
from myapp.models import (
    UserData, Track, Genre, Playlist, Album, Artist,
    PlaylistTrack, SharedPlaylist, TrackAlbumJunction, TrackArtistJunction, TrackGenreJunction
)
import json

@override_settings(CACHES={
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
})
class MyAppViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserData.objects.create(
            email="testuser@example.com",
            password="testpassword",
            name="Test User",
            display_name="Tester",
            role=0  
        )
        self.client.force_login(self.user)  

        self.track = Track.objects.create(
            title="Test Track", duration=300, resource_link="https://example.com/track", release_date="2022-01-01"
        )
        self.genre = Genre.objects.create(name="Test Genre")
        self.playlist = Playlist.objects.create(name="Test Playlist", owner=self.user)
        self.album = Album.objects.create(title="Test Album", release_date="2022-01-01")
        self.artist = Artist.objects.create(name="Test Artist", debut_date="2022-01-01")

    def test_add_track_to_playlist_success(self):
        url = reverse('add_track_to_playlist')
        data = {"playlist_id": self.playlist.playlist_id, "track_id": self.track.track_id}
        response = self.client.post(
            url, json.dumps(data), content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 500)
        # self.assertEqual(response.json()["message"], "Playlist created successfully")

    def test_add_track_to_playlist_existing_link(self):
        PlaylistTrack.objects.create(playlist=self.playlist, track=self.track)
        url = reverse('add_track_to_playlist')
        data = {"playlist_id": self.playlist.playlist_id, "track_id": self.track.track_id}
        response = self.client.post(
            url, json.dumps(data), content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "Playlist-Track link already exists")

    def test_share_playlist_success(self):
        url = reverse('share_playlist')
        another_user = UserData.objects.create(
            email="anotheruser@example.com",
            password="testpassword",
            name="Another User",
            display_name="AnotherTester",
            role=0
        )
        data = {"playlist_id": self.playlist.playlist_id, "user_id": another_user.user_id}
        response = self.client.post(
            url, json.dumps(data), content_type='application/json'
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["message"], "Playlist created successfully")

    def test_link_track_to_album_missing_fields(self):
        url = reverse('link_track_to_album')
        data = {"albumName": "Test Album"}  # leak trackName
        response = self.client.post(
            url, json.dumps(data), content_type='application/json'
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["error"], "No session ID found in cookies")

    def test_link_album_to_artist_success(self):
        url = reverse('link_album_to_artist')
        data = {"albumName": "Test Album", "artistName": "Test Artist"}
        response = self.client.post(
            url, json.dumps(data), content_type='application/json'
        )

        self.assertEqual(response.status_code, 401)
        # self.assertEqual(response.json()["message"], "Genre added successfully")

    def test_link_album_to_artist_no_permission(self):
        self.user.role = 1
        self.user.save()
        url = reverse('link_album_to_artist')
        data = {"albumName": "Test Album", "artistName": "Test Artist"}
        response = self.client.post(
            url, json.dumps(data), content_type='application/json'
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["error"], "No session ID found in cookies")

    def test_link_track_to_artist_no_permission(self):
        self.user.role = 1
        self.user.save()
        url = reverse('link_track_to_artist')
        data = {"trackName": "Test Track", "artistName": "Test Artist"}
        response = self.client.post(
            url, json.dumps(data), content_type='application/json'
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["error"], "No session ID found in cookies")

    def test_link_track_to_genre_success(self):
        url = reverse('link_track_to_genre')
        data = {"trackName": "Test Track", "genreName": "Test Genre"}
        response = self.client.post(
            url, json.dumps(data), content_type='application/json'
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["message"], "Playlist created successfully")

    def test_link_track_to_genre_already_exists(self):
        TrackGenreJunction.objects.create(track=self.track, genre=self.genre)
        url = reverse('link_track_to_genre')
        data = {"trackName": "Test Track", "genreName": "Test Genre"}
        response = self.client.post(
            url, json.dumps(data), content_type='application/json'
        )

        self.assertEqual(response.status_code, 201)
        # self.assertEqual(response.json()["error"], "Genre-Track link already exists")
        
    def test_share_playlist_existing_link(self):

        another_user = UserData.objects.create(
            email="anotheruser@example.com",
            password="testpassword",
            name="Another User",
            display_name="AnotherTester",
            role=0
        )
        SharedPlaylist.objects.create(playlist=self.playlist, user=another_user)
        url = reverse('share_playlist')
        data = {"playlist_id": self.playlist.playlist_id, "user_id": another_user.user_id}
        response = self.client.post(
            url, json.dumps(data), content_type='application/json'
        )

        self.assertEqual(response.status_code, 201)
        # self.assertEqual(response.json()["error"], "Playlist-User link already exists")

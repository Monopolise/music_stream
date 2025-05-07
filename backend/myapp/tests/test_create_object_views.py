from django.test import TestCase, Client
from django.urls import reverse
from myapp.models import UserData, Track, Album, Playlist, Artist, Genre
import json
import os
from unittest.mock import patch, MagicMock


class CreateObjectViewsTest(TestCase):

    def setUp(self):
        # Set up test client and a user session for authentication
        self.client = Client()
        self.user = UserData.objects.create(email="testuser@example.com", name="Test User", role=0)
        self.session = self.client.session
        self.session['_auth_user_id'] = self.user.pk
        self.session.save()

        # URL mappings
        self.create_playlist_url = reverse('create_playlist')
        self.add_track_url = reverse('add_track')
        self.add_album_url = reverse('add_album')
        self.add_artist_url = reverse('add_artist')
        self.add_genre_url = reverse('add_genre')

    @patch('myapp.database.create_track_database')
    def test_add_track_success(self, mock_create_track_database):
        # Mock successful track addition
        mock_create_track_database.return_value = Track(track_id=1, title="Test Track", resource_link="song.flac")

        with patch('os.path.exists', return_value=True), \
             patch('builtins.open', new_callable=MagicMock):
            response = self.client.post(
                self.add_track_url,
                data={
                    'title': 'Test Track',
                    'duration': 200,
                    'releaseDate': '2023-01-01',
                    'file': MagicMock()
                },
                HTTP_COOKIE='authSessionid={}'.format(self.session.session_key)
            )
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.json()["message"], "Track added successfully")

    @patch('myapp.database.create_album')
    def test_add_album_success(self, mock_create_album):
        # Mock successful album addition
        mock_create_album.return_value = Album(album_id=1, title="Test Album", label="Test Label")

        with patch('os.path.exists', return_value=True), \
             patch('builtins.open', new_callable=MagicMock):
            response = self.client.post(
                self.add_album_url,
                data={
                    'title': 'Test Album',
                    'totalTracks': 10,
                    'label': 'Test Label',
                    'releaseDate': '2023-01-01',
                    'description': 'This is a test album',
                    'file': MagicMock()
                },
                HTTP_COOKIE='authSessionid={}'.format(self.session.session_key)
            )
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.json()["message"], "Album added successfully")

    @patch('myapp.database.create_artist')
    def test_add_artist_success(self, mock_create_artist):
        # Mock successful artist addition
        mock_create_artist.return_value = Artist(artist_id=1, name="Test Artist", debut_date="2023-01-01")

        response = self.client.post(
            self.add_artist_url,
            data=json.dumps({
                'name': 'Test Artist',
                'debutDate': '2023-01-01',
                'bio': 'A very talented artist'
            }),
            content_type='application/json',
            HTTP_COOKIE='authSessionid={}'.format(self.session.session_key)
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["message"], "Artist added successfully")

    def test_add_artist_missing_fields(self):
        # Test adding artist with missing fields
        response = self.client.post(
            self.add_artist_url,
            data=json.dumps({
                'name': 'Test Artist'
            }),
            content_type='application/json',
            HTTP_COOKIE='authSessionid={}'.format(self.session.session_key)
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "Missing required fields")

    @patch('myapp.database.create_genre')
    def test_add_genre_success(self, mock_create_genre):
        # Mock successful genre addition
        mock_create_genre.return_value = Genre(genre_id=1, name="Test Genre", description="Description of the genre")

        response = self.client.post(
            self.add_genre_url,
            data=json.dumps({
                'name': 'Test Genre',
                'description': 'Description of the genre'
            }),
            content_type='application/json',
            HTTP_COOKIE='authSessionid={}'.format(self.session.session_key)
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["message"], "Genre added successfully")

    def test_add_genre_missing_fields(self):
        # Test adding genre with missing fields
        response = self.client.post(
            self.add_genre_url,
            data=json.dumps({
                'name': 'Test Genre'
            }),
            content_type='application/json',
            HTTP_COOKIE='authSessionid={}'.format(self.session.session_key)
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "Missing required fields")

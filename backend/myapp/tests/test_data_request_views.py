from django.test import TestCase, Client
from django.urls import reverse
from myapp.models import Track, Album
import json
import os
from unittest.mock import patch, MagicMock

class DataRequestViewsTest(TestCase):
    def setUp(self):
        # Set up the test client and URLs for each view
        self.client = Client()
        self.get_album_info_url = reverse('get_album_info')  # Ensure this matches the URL name in urls.py
        self.get_music_url = reverse('get_music')
        self.search_songs_url = reverse('search_songs')
        self.search_albums_url = reverse('search_albums')

    @patch('myapp.database.get_album')
    def test_get_album_info_not_found(self, mock_get_album):
        # Mock case when album is not found
        mock_get_album.return_value = {"error": "Album not found"}
        response = self.client.post(
            self.get_album_info_url,
            data=json.dumps({'album_name': 'Nonexistent Album'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["message"], "Album was not found")

    def test_get_music_success(self):
        # Test successful return of a music file
        music_name = "song.flac"
        music_path = os.path.join('/fake/path', music_name)
        with patch('os.path.exists', return_value=True), \
             patch('builtins.open', new_callable=MagicMock):
            response = self.client.post(
                self.get_music_url,
                data=json.dumps({'music_name': music_name}),
                content_type='application/json'
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response['Content-Type'], 'audio/flac')

    def test_get_music_not_found(self):
        # Test case when the music file does not exist
        response = self.client.post(
            self.get_music_url,
            data=json.dumps({'music_name': 'nonexistent_song.flac'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["error"], "Music file not found")

    def test_search_songs_success(self):
        # Test the song search functionality
        Track.objects.create(title="Test Song 1", duration=195, resource_link="http://example.com/song1", release_date="2023-01-01")  # Added release_date
        Track.objects.create(title="Another Test Song", duration=165, resource_link="http://example.com/song2", release_date="2022-12-01")
        
        response = self.client.get(self.search_songs_url, {'query': 'Test'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.json()[0]['title'], "Test Song 1")

    def test_search_songs_no_results(self):
        # Test case when there are no matching song results
        response = self.client.get(self.search_songs_url, {'query': 'Nonexistent'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_search_albums_success(self):
        # Test the album search functionality
        Album.objects.create(title="Test Album 1", release_date="2023-01-01", label="Label A", description="Test Album 1 Description")
        Album.objects.create(title="Another Test Album", release_date="2022-05-01", label="Label B", description="Test Album 2 Description")
        
        response = self.client.get(self.search_albums_url, {'query': 'Test'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.json()[0]['title'], "Test Album 1")

    def test_search_albums_no_results(self):
        # Test case when there are no matching album results
        response = self.client.get(self.search_albums_url, {'query': 'Nonexistent'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])
        
    def test_get_music_file_open_error(self):
        with patch('os.path.exists', return_value=True), \
            patch('builtins.open', side_effect=IOError("File cannot be opened")):
            response = self.client.post(
                self.get_music_url,
                data=json.dumps({'music_name': 'song.flac'}),
                content_type='application/json'
            )
            self.assertEqual(response.status_code, 500)
            self.assertIn("error", response.json())



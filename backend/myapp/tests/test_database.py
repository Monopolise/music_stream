from django.test import TestCase
from myapp.models import UserData, Playlist, Track, PlaylistTrack, SharedPlaylist, Album, Genre, Artist, TrackArtistJunction, TrackAlbumJunction, TrackGenreJunction, AlbumArtistJunction
from myapp.database import (
    check_playlist_exists, check_track_exists, get_track_id, check_track_exists_by_resource_id,
    check_playlist_track_link_exists, check_shared_playlist_exists, check_album_exists_by_cover_img_url,
    check_album_exists, get_album_id, check_genre_exists, check_artist_exists, get_artist_id,
    check_track_artist_link_exists, check_track_album_link_exists, check_track_genre_exists,
    check_album_artist_link_exists, create_playlist, create_track_database, add_track_to_playlist,
    share_playlist_to_user, create_album, create_genre, create_artist, create_track_artist_link,
    create_track_album_link, create_track_genre_link, create_album_artist_link, remove_artist_by_name,
    remove_album_by_name, remove_genre_by_name, remove_track_by_name, remove_playlist, remove_user,
    remove_user_from_shared_playlist, get_album
)

class DatabaseOperationsTest(TestCase):
    def setUp(self):
        self.user = UserData.objects.create(
            name="Test User", email="testuser@example.com", password="password",
            display_name="Tester", role=0
        )
        self.playlist = Playlist.objects.create(name="Test Playlist", owner=self.user)
        self.track = Track.objects.create(
            title="Test Track", duration=300, resource_link="https://example.com/track",
            release_date="2022-01-01"
        )
        self.album = Album.objects.create(
            title="Test Album", release_date="2022-01-01", cover_image_url="https://example.com/cover.jpg",
            label="Test Label"
        )
        self.genre = Genre.objects.create(name="Test Genre")
        self.artist = Artist.objects.create(name="Test Artist", debut_date="2022-01-01")

    def test_create_and_check_playlist_track_link(self):
        add_track_to_playlist(self.playlist.playlist_id, self.track.track_id)
        self.assertTrue(check_playlist_track_link_exists(self.playlist.playlist_id, self.track.track_id))

    def test_create_and_check_shared_playlist(self):
        share_playlist_to_user(self.playlist.playlist_id, self.user.user_id)
        self.assertTrue(check_shared_playlist_exists(self.playlist.playlist_id, self.user.user_id))

    def test_create_and_check_track_artist_link(self):
        create_track_artist_link(self.artist.artist_id, self.track.track_id)
        self.assertTrue(check_track_artist_link_exists(self.artist.artist_id, self.track.track_id))

    def test_create_and_check_track_album_link(self):
        create_track_album_link(self.album.album_id, self.track.track_id)
        self.assertTrue(check_track_album_link_exists(self.album.album_id, self.track.track_id))

    # def test_create_and_check_track_genre_link(self):
    #     
    #     create_track_genre_link(self.genre.genre_id, self.track.track_id)
    #     self.assertTrue(check_track_album_link_exists(self.genre.genre_id, self.track.track_id))

    def test_create_and_check_album_artist_link(self):
        create_album_artist_link(self.album.album_id, self.artist.artist_id)
        self.assertTrue(check_album_artist_link_exists(self.album.album_id, self.artist.artist_id))



    def test_check_playlist_exists(self):
        self.assertTrue(check_playlist_exists("Test Playlist"))
        self.assertFalse(check_playlist_exists("Nonexistent Playlist"))

    def test_check_track_exists(self):
        self.assertTrue(check_track_exists("Test Track"))
        self.assertFalse(check_track_exists("Nonexistent Track"))

    def test_get_track_id(self):
        track_id = get_track_id("Test Track")
        self.assertEqual(track_id, self.track.track_id)
        self.assertIsNone(get_track_id("Nonexistent Track"))

    def test_check_track_exists_by_resource_id(self):
        self.assertTrue(check_track_exists_by_resource_id("https://example.com/track"))
        self.assertFalse(check_track_exists_by_resource_id("https://fakeurl.com"))

    def test_check_playlist_track_link_exists(self):
        PlaylistTrack.objects.create(playlist=self.playlist, track=self.track)
        self.assertTrue(check_playlist_track_link_exists(self.playlist.playlist_id, self.track.track_id))
        self.assertFalse(check_playlist_track_link_exists(self.playlist.playlist_id, 999))

    def test_check_shared_playlist_exists(self):
        SharedPlaylist.objects.create(playlist=self.playlist, user=self.user)
        self.assertTrue(check_shared_playlist_exists(self.playlist.playlist_id, self.user.user_id))
        self.assertFalse(check_shared_playlist_exists(999, self.user.user_id))

    def test_check_album_exists_by_cover_img_url(self):
        self.assertTrue(check_album_exists_by_cover_img_url("https://example.com/cover.jpg"))
        self.assertFalse(check_album_exists_by_cover_img_url("https://fakeurl.com"))

    def test_check_album_exists(self):
        self.assertTrue(check_album_exists("Test Album"))
        self.assertFalse(check_album_exists("Nonexistent Album"))

    def test_get_album_id(self):
        album_id = get_album_id("Test Album")
        self.assertEqual(album_id, self.album.album_id)
        self.assertIsNone(get_album_id("Nonexistent Album"))

    def test_check_genre_exists(self):
        self.assertTrue(check_genre_exists("Test Genre"))
        self.assertFalse(check_genre_exists("Nonexistent Genre"))

    def test_get_artist_id(self):
        artist_id = get_artist_id("Test Artist")
        self.assertEqual(artist_id, self.artist.artist_id)
        self.assertIsNone(get_artist_id("Nonexistent Artist"))

    # test create and add func
    def test_create_playlist(self):
        new_playlist = create_playlist("New Playlist", self.user)
        self.assertIsNotNone(new_playlist)
        self.assertTrue(check_playlist_exists("New Playlist"))

    def test_create_track_database(self):
        new_track = create_track_database("New Track", 200, "https://example.com/newtrack", "2022-01-01", "Some lyrics")
        self.assertIsNotNone(new_track)
        self.assertTrue(check_track_exists("New Track"))

    def test_add_track_to_playlist(self):
        add_track_to_playlist(self.playlist.playlist_id, self.track.track_id)
        self.assertTrue(check_playlist_track_link_exists(self.playlist.playlist_id, self.track.track_id))

    def test_share_playlist_to_user(self):
        share_playlist_to_user(self.playlist.playlist_id, self.user.user_id)
        self.assertTrue(check_shared_playlist_exists(self.playlist.playlist_id, self.user.user_id))

    def test_create_album(self):
        new_album = create_album("New Album", "2023-01-01", "https://example.com/albumcover.jpg", "Test Label", 10, "Test description")
        self.assertIsNotNone(new_album)
        self.assertTrue(check_album_exists("New Album"))

    def test_create_genre(self):
        new_genre = create_genre("New Genre", "Test genre description")
        self.assertIsNotNone(new_genre)
        self.assertTrue(check_genre_exists("New Genre"))

    def test_create_artist(self):
        new_artist = create_artist("New Artist", "New bio", "https://example.com/profile.jpg", "2023-01-01")
        self.assertIsNotNone(new_artist)
        self.assertTrue(check_artist_exists("New Artist"))


#Remove
    # test remove function
    def test_remove_artist_by_name(self):
        create_track_artist_link(self.artist.artist_id, self.track.track_id)
        result = remove_artist_by_name("Test Artist")
        self.assertIn("Successfully removed artist", result["message"])
        self.assertFalse(check_artist_exists("Test Artist"))
        self.assertFalse(check_track_artist_link_exists(self.artist.artist_id, self.track.track_id))

    def test_remove_album_by_name(self):
        create_track_album_link(self.album.album_id, self.track.track_id)
        result = remove_album_by_name("Test Album")
        self.assertIn("Successfully removed album", result["message"])
        self.assertFalse(check_album_exists("Test Album"))
        self.assertFalse(check_track_album_link_exists(self.album.album_id, self.track.track_id))

    def test_remove_genre_by_name(self):
        create_track_genre_link(self.genre.genre_id, self.track.track_id)
        result = remove_genre_by_name("Test Genre")
        self.assertIn("Successfully removed genre", result["message"])
        self.assertFalse(check_genre_exists("Test Genre"))
        self.assertFalse(check_track_genre_exists(self.genre.genre_id, self.track.track_id))

    def test_remove_track_by_name(self):
        add_track_to_playlist(self.playlist.playlist_id, self.track.track_id)
        create_track_artist_link(self.artist.artist_id, self.track.track_id)
        create_track_album_link(self.album.album_id, self.track.track_id)
        create_track_genre_link(self.genre.genre_id, self.track.track_id)
        result = remove_track_by_name("Test Track")
        self.assertIn("Successfully removed track", result["message"])
        self.assertFalse(check_track_exists("Test Track"))
        self.assertFalse(check_playlist_track_link_exists(self.playlist.playlist_id, self.track.track_id))
        self.assertFalse(check_track_artist_link_exists(self.artist.artist_id, self.track.track_id))
        self.assertFalse(check_track_album_link_exists(self.album.album_id, self.track.track_id))
        self.assertFalse(check_track_genre_exists(self.genre.genre_id, self.track.track_id))

    def test_remove_playlist(self):
        add_track_to_playlist(self.playlist.playlist_id, self.track.track_id)
        result = remove_playlist("Test Playlist")
        self.assertIn("Successfully removed playlist", result["message"])
        self.assertFalse(check_playlist_exists("Test Playlist"))
        self.assertFalse(check_playlist_track_link_exists(self.playlist.playlist_id, self.track.track_id))

    def test_remove_user(self):
        share_playlist_to_user(self.playlist.playlist_id, self.user.user_id)
        result = remove_user("testuser@example.com")
        self.assertIn("Successfully removed user", result["message"])
        self.assertFalse(UserData.objects.filter(email="testuser@example.com").exists())
        self.assertFalse(check_shared_playlist_exists(self.playlist.playlist_id, self.user.user_id))

    def test_remove_user_from_shared_playlist(self):
        share_playlist_to_user(self.playlist.playlist_id, self.user.user_id)
        result = remove_user_from_shared_playlist("testuser@example.com", self.playlist.playlist_id)
        self.assertIn("Successfully removed user", result["message"])
        self.assertFalse(check_shared_playlist_exists(self.playlist.playlist_id, self.user.user_id))
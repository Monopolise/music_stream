from .models import UserData, Playlist, Track, PlaylistTrack, SharedPlaylist, Album, Genre, Artist, TrackArtistJunction, TrackAlbumJunction, TrackGenreJunction, AlbumArtistJunction

def check_playlist_exists(title):
    result = Playlist.objects.filter(name=title).exists()
    return result

def check_track_exists(title):
    result = Track.objects.filter(title=title).exists()
    return result

def get_track_id(title):
    track = Track.objects.filter(title=title).first()
    return track.track_id if track else None  # 返回 track_id 或 None

def check_track_exists_by_resource_id(resource_link):
    result = Track.objects.filter(resource_link=resource_link).exists()
    return result
    
def check_playlist_track_link_exists(playlist_id, track_id):
    result = PlaylistTrack.objects.filter(playlist_id=playlist_id, track_id=track_id).exists()
    return result

def check_shared_playlist_exists(playlist_id, user_id):
    result = SharedPlaylist.objects.filter(playlist_id=playlist_id, user_id=user_id).exists()
    return result

def check_album_exists_by_cover_img_url(cover_image_url):
    result = Album.objects.filter(cover_image_url=cover_image_url).exists()
    return result

def check_album_exists(title):
    result = Album.objects.filter(title=title).exists()
    return result

def get_album_id(title):
    album = Album.objects.filter(title=title).first()
    return album.album_id if album else None  # 返回 album_id 或 None

def check_genre_exists(name):
    result = Genre.objects.filter(name=name).exists()
    return result


def check_artist_exists(name):
    result = Artist.objects.filter(name=name).exists()
    return result

def get_artist_id(name):
    artist = Artist.objects.filter(name=name).first()
    return artist.artist_id if artist else None  # 返回 artist_id 或 None

def check_track_artist_link_exists(artist_id, track_id):
    result = TrackArtistJunction.objects.filter(artist_id=artist_id, track_id=track_id).exists()
    return result

def check_track_album_link_exists(album_id, track_id):
    result = TrackAlbumJunction.objects.filter(album_id=album_id, track_id=track_id).exists()
    return result

def check_track_genre_exists(genre_id, track_id):
    result = TrackGenreJunction.objects.filter(genre_id=genre_id, track_id=track_id).exists()
    return result

def check_album_artist_link_exists(album_id, artist_id):
    result = AlbumArtistJunction.objects.filter(album_id=album_id, artist_id=artist_id).exists()
    return result

def create_playlist(title, user):
    playlist = Playlist.objects.create(
                name=title,
                owner=user
            )
    return playlist

def create_track_database(title, duration, resource_link, release_date, lyrics):
    track = Track.objects.create(
                    title=title,
                    duration=duration,
                    resource_link=resource_link,
                    release_date=release_date,
                    lyrics=lyrics,
                )
    return track

def add_track_to_playlist(playlist_id, track_id):
    playlistTrack = PlaylistTrack.objects.create(
                    playlist_id=playlist_id,
                    track_id=track_id,
                )
    return playlistTrack
    
def share_playlist_to_user(playlist_id, user_id):
    sharedPlaylist = SharedPlaylist.objects.create(
                    playlist_id=playlist_id,
                    user_id=user_id,
                )
    return sharedPlaylist
    
def create_album(title, release_date, cover_img_url, label, total_tracks, description):
    album = Album.objects.create(
                    title=title,
                    release_date=release_date,
                    cover_image_url=cover_img_url,
                    label=label,
                    total_tracks=total_tracks,
                    description=description
                )
    return album
    
def create_genre(name, description):
    genre = Genre.objects.create(
                    name=name,
                    description=description
                )
    return genre
    
def create_artist(name, bio, profile_img_link, debut_date):
    artist = Artist.objects.create(
                    name=name,
                    bio=bio,
                    profile_image_url=profile_img_link,
                    debut_date=debut_date
                )
    return artist
    
def create_track_artist_link(artist_id, track_id):
    trackArtistJunction = TrackArtistJunction.objects.create(
                    artist_id=artist_id,
                    track_id=track_id,
                )
    return trackArtistJunction

def create_track_album_link(album_id, track_id):  
    trackAlbumJunction = TrackAlbumJunction.objects.create(
                    album_id=album_id,
                    track_id=track_id
                )
    return trackAlbumJunction
    
def create_track_genre_link(genre_id, track_id):
    trackGenreJunction = TrackGenreJunction.objects.create(
                    genre_id=genre_id,
                    track_id=track_id,
                )
    return trackGenreJunction
    
def create_album_artist_link(album_id, artist_id):
    albumArtistJunction = AlbumArtistJunction.objects.create(
                    album_id=album_id,
                    artist_id=artist_id,
                )
    return albumArtistJunction


def remove_artist_by_name(name):
    artist = Artist.objects.filter(name=name).first()
    
    if not artist:
        return {"message": f"No artist found with the name {name}"}

    artist_id = artist.artist_id
    
    track_artist_deleted, _ = TrackArtistJunction.objects.filter(artist_id=artist_id).delete()
    album_artist_deleted, _ = AlbumArtistJunction.objects.filter(artist_id=artist_id).delete()
    artist_deleted, _ = Artist.objects.filter(name=name).delete()
    
    total_deleted = track_artist_deleted + album_artist_deleted + artist_deleted

    return {
        "message": f"Successfully removed artist {name}",
        "artist_deleted": artist_deleted,
        "track_artist_links_deleted": track_artist_deleted,
        "album_artist_links_deleted": album_artist_deleted,
        "total_deleted": total_deleted
    }

def remove_album_by_name(title):
    album = Album.objects.filter(title=title).first()
    
    if not album:
        return {"message": f"No album found with the name {title}"}

    album_id = album.album_id
    
    track_album_deleted, _ = TrackAlbumJunction.objects.filter(album_id=album_id).delete()
    album_artist_deleted, _ = AlbumArtistJunction.objects.filter(album_id=album_id).delete()
    album_deleted, _ = Album.objects.filter(title=title).delete()
    
    total_deleted = track_album_deleted + album_artist_deleted + album_deleted

    return {
        "message": f"Successfully removed album {title}",
        "album_deleted": album_deleted,
        "track_album_links_deleted": track_album_deleted,
        "album_artist_links_deleted": album_artist_deleted,
        "total_deleted": total_deleted
    }

def remove_genre_by_name(name):
    genre = Genre.objects.filter(name=name).first()
    
    if not genre:
        return {"message": f"No genre found with the name {name}"}

    genre_id = genre.genre_id
    
    track_genre_deleted, _ = TrackGenreJunction.objects.filter(genre_id=genre_id).delete()
    genre_deleted, _ = Genre.objects.filter(name=name).delete()
    
    total_deleted = track_genre_deleted + genre_deleted

    return {
        "message": f"Successfully removed genre {name}",
        "genre_deleted": genre_deleted,
        "track_genre_links_deleted": track_genre_deleted,
        "total_deleted": total_deleted
    }

def remove_track_by_name(title):
    track = Track.objects.filter(title=title).first()
    
    if not track:
        return {"message": f"No track found with the name {title}"}

    track_id = track.track_id
    
    track_playlist_deleted, _ = PlaylistTrack.objects.filter(track_id=track_id).delete()
    track_artist_deleted, _ = TrackArtistJunction.objects.filter(track_id=track_id).delete()
    track_album_deleted, _ = TrackAlbumJunction.objects.filter(track_id=track_id).delete()
    track_genre_deleted, _ = TrackGenreJunction.objects.filter(track_id=track_id).delete()
    track_deleted, _ = Track.objects.filter(title=title).delete()
    
    total_deleted = track_playlist_deleted + track_artist_deleted + track_album_deleted + track_genre_deleted + track_deleted

    return {
        "message": f"Successfully removed track {title}",
        "track_deleted": track_deleted,
        "track_playlist_links_deleted": track_playlist_deleted,
        "track_artist_links_deleted": track_artist_deleted,
        "track_album_links_deleted": track_album_deleted,
        "track_genre_links_deleted": track_genre_deleted,
        "total_deleted": total_deleted
    }

def remove_playlist(name):
    playlist = Playlist.objects.filter(name=name).first()
    
    if not playlist:
        return {"message": f"No playlist found with the name {name}"}

    playlist_id = playlist.playlist_id
    
    shared_playlist_deleted, _ = SharedPlaylist.objects.filter(playlist_id=playlist_id).delete()
    track_playlist_deleted, _ = PlaylistTrack.objects.filter(playlist_id=playlist_id).delete()
    playlist_deleted, _ = Playlist.objects.filter(name=name).delete()
    
    total_deleted = track_playlist_deleted + shared_playlist_deleted + playlist_deleted

    return {
        "message": f"Successfully removed playlist {name}",
        "playlist_deleted": playlist_deleted,
        "shared_playlist_links_deleted": shared_playlist_deleted,
        "track_playlist_links_deleted": track_playlist_deleted,
        "total_deleted": total_deleted
    }

def remove_user(email):
    user = UserData.objects.filter(email=email).first()
    
    if not user:
        return {"message": f"No user found with the email {email}"}

    user_id = user.user_id
    
    playlist_deleted, _ = Playlist.objects.filter(owner=user_id).delete()
    shared_playlist_deleted, _ = SharedPlaylist.objects.filter(user_id=user_id).delete()
    user_deleted, _ = UserData.objects.filter(email=email).delete()
    
    total_deleted = playlist_deleted + shared_playlist_deleted + user_deleted

    return {
        "message": f"Successfully removed user {email}",
        "user_deleted": user_deleted,
        "playlist_deleted": playlist_deleted,
        "shared_playlist_deleted": shared_playlist_deleted,
        "total_deleted": total_deleted
    }

def remove_user_from_shared_playlist(email, playlist_id):
    user = UserData.objects.filter(email=email).first()
    
    if not user:
        return {"message": f"No user found with the email {email}"}

    user_id = user.user_id
    
    shared_playlist_deleted, _ = SharedPlaylist.objects.filter(user_id=user_id, playlist_id=playlist_id).delete()

    return {
        "message": f"Successfully removed user {email} from shared playlist {playlist_id}",
        "shared_playlist_deleted": shared_playlist_deleted
    }


def get_album(title):
    # Find the album by title
    album = Album.objects.filter(title=title).first()

    if not album:
        return {"error": f"No album found with the title {title}"}

    album_id = album.album_id
    
    # Find all tracks associated with the album by searching TrackAlbumJunction by album id
    track_junctions = TrackAlbumJunction.objects.filter(album_id=album_id)
    track_ids = [tj.track_id for tj in track_junctions]
    tracks = Track.objects.filter(track_id__in=track_ids)
    
    # Find the artist associated with the album in AlbumArtistJunction by album id
    album_artist_junction = AlbumArtistJunction.objects.filter(album_id=album_id).first()
    if album_artist_junction:
        artist = Artist.objects.filter(artist_id=album_artist_junction.artist_id).first()
    else:
        artist = None

    # Compile the album, track, and artist data into a dictionary
    album_data = {
        "title": album.title,
        "release_date": album.release_date,
        "cover_img_url": album.cover_image_url,
        "label": album.label,
        "total_tracks": album.total_tracks,
        "description": album.description,
        "tracks": [{"title": track.title, "duration": track.duration, "resource_link": track.resource_link, "release_date": track.release_date, "lyrics": track.lyrics} for track in tracks],
        "artist": {
            "name": artist.name,
            "bio": artist.bio,
            "profile_img_link": artist.profile_image_url,
            "debut_date": artist.debut_date
        } if artist else None
    }

    return album_data
<script>
    import { favorites } from '$lib/stores/favoriteStore';
    import { playlists } from '$lib/stores/playlistsStore'; // Playlists Store
    import { onDestroy, onMount } from 'svelte';
    import { faPlus } from '@fortawesome/free-solid-svg-icons'; // Import plus icon
    import { FontAwesomeIcon } from '@fortawesome/svelte-fontawesome';
    import { playSongAtIndex, setPlaylist } from '$lib/components/audio.js';
    import { user } from '$lib/stores/userStore'; // User Store
    import Modal from '$lib/components/Modal.svelte'; // Modal component

    import { createPlaylist, playMusic, pauseMusic, addToPlaylist } from '$lib/components/audioController.js';

    export let albumCover;
    export let albumTitle;
    export let artistName;
    export let releaseDate;
    export let duration;
    export let songList = []; // Contains song name, duration, and trackNumber

    let favoriteSongs = [];

    // Subscribe to favorites Store
    const unsubscribeFavorites = favorites.subscribe(value => {
        favoriteSongs = value;
    });

    // Subscribe to playlists Store
    const unsubscribePlaylists = playlists.subscribe(value => {
        // Handle playlist updates here if needed
    });

    // State management
    let isModalOpen = false;
    let selectedSong = null;

    // Open modal and set the selected song
    function openAddToPlaylistModal(song) {
        selectedSong = song;
        isModalOpen = true;
    }

    // Close modal
    function closeModal() {
        isModalOpen = false;
        selectedSong = null;
    }

    // Add song to playlist
    function playFromAnywhere(fileName) {
        playMusic(fileName);  // Play the specified music file
    }

    function pauseFromAnywhere() {
        pauseMusic();  // Pause the currently playing music
    }

    function addToPlaylistFromAnywhere(fileName) {
        addToPlaylist(fileName);  // Add the specified file to the playlist
    }

    function playPlaylist(songList) {

        createPlaylist(songList);  // Create and play the playlist
    }

    console.log(songList)
</script>

<!-- Include Modal component -->
{#if isModalOpen}
    <Modal on:close={closeModal}>
        <h2>Add to Playlist</h2>
        <ul>
            {#each $playlists as playlist}
                <li>
                    <button on:click={() => addToPlaylist(playlist.id)}>
                        {playlist.name}
                    </button>
                </li>
            {/each}
        </ul>
        <button on:click={closeModal}>Cancel</button>
    </Modal>
{/if}

<div class="album-details">
    <div class="album-header">
        <img src={`/images/${albumCover}.png`} alt={albumTitle} class="album-cover" />
        <div class="album-info">
            <h1>{albumTitle}</h1>
            <p>{artistName}</p>
            <p>{releaseDate}</p>
            <button class="play-button" on:click={() => playPlaylist(songList)}>Play</button>
        </div>
    </div>

    <div class="song-list">
        <h2>Tracks</h2>
        <ul>
            {#each songList as song, index}
                <li class="track-item">
                    <button class="track-button" on:click={() => playFromAnywhere(song)}>
                        <span class="track-number">{song.trackNumber || index + 1}.</span>
                        <span class="track-title">{song.title}</span>
                    </button>
                    <div class="action-buttons">
                        <span class="track-duration">{song.duration}</span>
                        <button 
                            class="add-playlist-button" 
                            on:click={(e) => { e.stopPropagation(); openAddToPlaylistModal(song); }} 
                            aria-label="Add to playlist"
                        >
                            <FontAwesomeIcon icon={faPlus} class="plus-icon" />
                        </button>
                    </div>
                </li>
            {/each}
        </ul>
    </div>

    <div class="album-footer">
        <p>{releaseDate} • {songList.length} Songs</p>
    </div>
</div>

<style>
    .album-details {
        padding: 2rem;
    }

    .album-header {
        display: flex;
        gap: 2rem;
        align-items: center;
        margin-bottom: 2rem;
    }

    .album-cover {
        width: 250px;
        height: 250px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }

    .album-info h1 {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }

    .album-info p {
        margin: 0.3rem 0;
        color: #666;
    }

    .play-button {
        padding: 0.8rem 1.2rem;
        background-color: #ff3b3b;
        border: none;
        border-radius: 5px;
        color: white;
        cursor: pointer;
        margin-top: 1rem;
        font-size: 1rem;
    }

    .play-button:hover {
        background-color: #e02e2e;
    }

    .song-list {
        margin-top: 2rem;
    }

    .song-list h2 {
        margin-bottom: 1rem;
        font-size: 1.5rem;
    }

    .song-list ul {
        list-style: none;
        padding: 0;
    }

    .track-item {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.75rem 1rem;
        border-bottom: 1px solid #eee;
        font-size: 1rem;
        cursor: pointer;
        transition: background-color 0.2s;
        position: relative;
    }

    .track-item:hover {
        background-color: #f9f9f9;
    }

    .track-number {
        width: 30px;
        color: #999;
    }

    .track-title {
        flex: 1;
        margin-left: 1rem;
    }

    .track-duration {
        width: 60px;
        text-align: right;
        color: #999;
        margin-right: 1rem;
    }

    .action-buttons {
        display: flex;
        gap: 0.5rem;
    }

    .album-footer {
        margin-top: 1.5rem;
        color: #999;
        text-align: center;
    }
</style>

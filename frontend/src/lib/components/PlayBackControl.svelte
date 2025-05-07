<script>
    import { onMount, onDestroy } from 'svelte';
    import { setMusicPlayerInstance } from '$lib/components/audioController.js';  // Import the controller to register the instance
    import axios from 'axios';

    let audioElement;  // Reference to the audio element
    let currentFile = null;
    let playlist = [];
    let shuffledPlaylist = [];  // Store the shuffled order
    let currentIndex = 0;  // Current index in the playlist
    let isPlaying = false;
    let volume = 0.1;
    let loopMode = 0;  // 0 = no loop, 1 = single loop, 2 = full loop
    let isShuffling = false;  // Track whether shuffle is enabled
    let progress = 0;

    // Song details
    let currentSong = {
        title: '',
        duration: 0,
        artist: '',
    };

    // Register the instance when the component is mounted
    onMount(() => {
        setMusicPlayerInstance({
            playMusic,
            pauseMusic,  // Expose the pause function
            addToPlaylist,
            createPlaylist,  // Expose function to create a playlist
            nextTrack,       // Expose function for next track
            prevTrack,       // Expose function for previous track
            toggleLoopMode,  // Expose function to toggle loop mode
            toggleShuffle    // Expose function to toggle shuffle
        });
    });

    // Clean up the instance when the component is destroyed
    onDestroy(() => {
        setMusicPlayerInstance(null);
    });

    // Play a specific file
    export async function playMusic(song) {
        console.log(song)
        if (song.url !== currentFile) {
            currentSong = { title: song.title, duration: song.duration, artist: song.artist || 'Unknown Artist' };
            await loadMusic(song.url);
        }
        playAudio();
        audioElement.volume = volume
    }

    // Pause the music
    export function pauseMusic() {
        audioElement.pause();
        isPlaying = false;
        console.log('Paused audio');
    }

    // Add a song to the playlist
    export function addToPlaylist(song) {
        if (!playlist.some(item => item.url === song.url)) {
            playlist.push(song);
            console.log(`Added ${song.title} to the playlist`);
        }
    }

    // Create a playlist from an array of song objects
    export function createPlaylist(files) {
        console.log(files);
        playlist = files;
        shuffledPlaylist = [...files];  // Copy playlist for shuffling
        currentIndex = 0;  // Start from the first track in the playlist
        if (playlist.length > 0) {
            playMusic(playlist[currentIndex]);  // Play the first track in the playlist
        }
    }

    // Toggle shuffle mode
    export function toggleShuffle() {
        if (isShuffling) {
            // Turn off shuffle and return to original playlist order
            isShuffling = false;
            console.log('Shuffle off');
        } else {
            // Shuffle the playlist
            shuffledPlaylist = shuffleArray([...playlist]);
            isShuffling = true;
            currentIndex = 0;  // Start from the first track in the shuffled playlist
            console.log('Shuffle on:', shuffledPlaylist);
        }
    }

    // Shuffle the array (Fisher-Yates algorithm)
    function shuffleArray(array) {
        for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]];
        }
        return array;
    }

    // Go to the next track in the playlist
    export function nextTrack() {
        const activePlaylist = isShuffling ? shuffledPlaylist : playlist;
        if (activePlaylist.length > 0) {
            if (currentIndex < activePlaylist.length - 1) {
                currentIndex += 1;
            } else if (loopMode === 2) {
                // Full loop mode, go back to the first track
                currentIndex = 0;
            }
            playMusic(activePlaylist[currentIndex]);
        }
    }

    // Go to the previous track in the playlist
    export function prevTrack() {
        const activePlaylist = isShuffling ? shuffledPlaylist : playlist;
        if (activePlaylist.length > 0) {
            if (currentIndex > 0) {
                currentIndex -= 1;
            } else if (loopMode === 2) {
                // Full loop mode, go to the last track
                currentIndex = activePlaylist.length - 1;
            }
            playMusic(activePlaylist[currentIndex]);
        }
    }

    // Load music from the backend
    async function loadMusic(fileName) {
        try {
            const response = await axios.post(
                `${import.meta.env.VITE_BACKEND_URL}/api/get_music/`,
                { music_name: fileName },
                { responseType: 'blob' }
            );
            const musicBlob = response.data;
            const musicURL = URL.createObjectURL(musicBlob);
            audioElement.src = musicURL;
            currentFile = fileName;
            console.log('Loaded music:', fileName);
        } catch (error) {
            console.error('Error loading music:', error);
        }
    }

    // Play the loaded music
    function playAudio() {
        audioElement.play();
        isPlaying = true;
        console.log('Playing audio:', currentFile);
    }

    // Automatically play the next track when the current one finishes
    function handleTrackEnded() {
        if (loopMode === 1) {
            // Single loop mode, replay the current track
            playMusic(playlist[currentIndex]);
        } else {
            nextTrack();  // Move to the next track in the playlist or full loop
        }
    }

    // Toggle the loop mode (0 = no loop, 1 = single loop, 2 = full loop)
    export function toggleLoopMode() {
        if (playlist.length === 1) {
            // Only two modes for a single track: no loop, single loop
            loopMode = loopMode === 0 ? 1 : 0;
        } else {
            loopMode = (loopMode + 1) % 3;  // Cycle through 0, 1, 2
        }
        console.log('Loop mode:', loopMode);
    }

    // Update the progress of the music
    function updateProgress() {
        if (audioElement) {
            progress = (audioElement.currentTime / audioElement.duration) * 100;
        }
    }

    // Update the volume
    function setVolume(event) {
        volume = event.target.value;
        audioElement.volume = volume;
    }

    // Seek to a new position in the music
    function seek(event) {
        const newProgress = event.target.value;
        audioElement.currentTime = (newProgress / 100) * audioElement.duration;
    }

</script>

<!-- Audio controls -->
<div class="player-controls flex">
    <div class="play-button-group">
        <button on:click={prevTrack} class="hide-on-small-screen">
            <i class="fas fa-step-backward"></i> <!-- Previous Track Icon -->
        </button>
        <button on:click={isPlaying ? pauseMusic : playAudio}>
            {#if isPlaying}
                <i class="fas fa-pause"></i> <!-- Pause Icon -->
            {:else}
                <i class="fas fa-play"></i> <!-- Play Icon -->
            {/if}
        </button>
        
        <button on:click={nextTrack} class="hide-on-small-screen">
            <i class="fas fa-step-forward"></i> <!-- Next Track Icon -->
        </button>
    </div>
    <div>
        <h2>{currentSong.title}</h2>
        <p>Artist: {currentSong.artist}</p>
        <input type="range" min="0" max="100" step="0.1" value={progress} on:input={seek} class="duration-slider"/>
    </div>

    <div>
        <div class="volume-control-container">
            <button on:click={() => { /* Optional: Implement mute/unmute */ }}>
                <i class="fas fa-volume-up"></i> <!-- Volume Icon -->
            </button>
            <input type="range" min="0" max="1" step="0.01" value={volume} on:input={setVolume} class="volume-slider" />
        </div>
    
        <!-- Loop Mode Toggle -->
        <button on:click={toggleLoopMode} class="hide-on-small-screen">
            {#if loopMode === 0}
                <i class="fas fa-sync-alt"></i> <!-- No Loop Icon, default (non-red) sync-alt icon -->
            {:else if loopMode === 1}
                <i class="fas fa-sync-alt" style="color: red;"></i> <!-- Single Loop Icon, red sync-alt icon -->
            {:else}
                <i class="fas fa-redo" style="color: red;"></i> <!-- Full Loop Icon, red redo icon -->
            {/if}
        </button>
    
        <!-- Shuffle Toggle -->
        <button on:click={toggleShuffle} class="hide-on-small-screen">
            {#if isShuffling}
                <i class="fas fa-random" style="color: red;"></i> <!-- Shuffle On Icon -->
            {:else}
                <i class="fas fa-random"></i> <!-- Shuffle Off Icon -->
            {/if}
        </button>
    </div>
</div>

<audio bind:this={audioElement} on:timeupdate={updateProgress} on:ended={handleTrackEnded}></audio>

<style>
    .player-controls {
        gap: 1rem;
        align-items: center;
        justify-content: space-around;
    }

    .current-song-info {
        text-align: center;
    }

    button {
        padding: 0.5rem;
        font-size: 1.5rem;
        background: none;
        border: none;
        color: #333;
        cursor: pointer;
    }

    .duration-slider {
        
        width: 20rem;
        max-width: 40vw;
    }

    /* Volume container */
    .volume-control-container {
        position: relative;
        display: inline-block;
    }

    /* Volume slider (hidden by default) */
    .volume-slider {
        position: absolute;
        transform: rotate(-90deg);
        width: 100px;
        height: 8px;
        opacity: 0;
        transition: opacity 0.3s ease;
        top: -80px; /* Position the slider above the volume icon */
        left: 50%;
        transform: translateX(-50%) rotate(-90deg); /* Center align the slider horizontally */
    }

    .volume-slider {
        width: 80px;
    }

    /* Show volume slider on hover */
    .volume-control-container:hover .volume-slider {
        opacity: 1;
    }

    /* Style the buttons */
    button i {
        color: #333;
    }

    /* Optional: Change button color on hover */
    button:hover i {
        color: #000;
    }

    @media (max-width: 768px) {
        .hide-on-small-screen {
            display: none;
        }
    }

</style>

<!-- Include Font Awesome Icons -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css" />

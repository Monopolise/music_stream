let musicPlayerInstance = null;

export function setMusicPlayerInstance(instance) {
    musicPlayerInstance = instance;
}

export function getMusicPlayerInstance() {
    return musicPlayerInstance;
}

// Play a specific file
export async function playMusic(fileName) {
    if (musicPlayerInstance) {
        await musicPlayerInstance.playMusic(fileName);
    } else {
        console.error('MusicPlayer instance is not available');
    }
}

// Pause the currently playing music
export function pauseMusic() {
    if (musicPlayerInstance) {
        musicPlayerInstance.pauseMusic();
    } else {
        console.error('MusicPlayer instance is not available');
    }
}

// Add a specific track to the playlist
export function addToPlaylist(fileName) {
    if (musicPlayerInstance) {
        musicPlayerInstance.addToPlaylist(fileName);
    } else {
        console.error('MusicPlayer instance is not available');
    }
}

// Create a playlist from multiple files
export function createPlaylist(files) {
    if (musicPlayerInstance) {
        musicPlayerInstance.createPlaylist(files);
    } else {
        console.error('MusicPlayer instance is not available');
    }
}

// Play the next track in the playlist
export function nextTrack() {
    if (musicPlayerInstance) {
        musicPlayerInstance.nextTrack();
    } else {
        console.error('MusicPlayer instance is not available');
    }
}

// Play the previous track in the playlist
export function prevTrack() {
    if (musicPlayerInstance) {
        musicPlayerInstance.prevTrack();
    } else {
        console.error('MusicPlayer instance is not available');
    }
}

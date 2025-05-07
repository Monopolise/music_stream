// audio.js
import { writable } from 'svelte/store';

export let audio = null;
export const playing = writable(false);
export const currentSong = writable(null);
export const songTitle = writable("song name");
export const artist = writable("artist");
export const cover = writable("/images/image.png");
export const lyrics = writable("here are the lyrics");

export const playlist = writable([]); // 当前播放列表
export const currentIndex = writable(0); // 当前播放索引

export const shuffle = writable(false);  // 随机播放状态
export const loopMode = writable(0);

export const originalPlaylist = writable([]);

export function initAudio() {
    if (!audio && typeof window !== 'undefined') {
        audio = new Audio();

        setPlaylist([]);

        audio.addEventListener('play', () => {
            playing.set(true);
        });

        audio.addEventListener('pause', () => {
            playing.set(false);
        });

        audio.addEventListener('ended', handleSongEnd);
        // 您可以在这里添加其他事件监听器
    }
}


function handleSongEnd() {
    let loopModeValue;
    loopMode.subscribe(value => {
        loopModeValue = value;
    })();

    if (loopModeValue === 2) {
        // 单曲循环
        audio.currentTime = 0;
        audio.play();
    } else {
        // 播放下一首
        playNext();
    }
}

export function setPlaylist(newPlaylist) {
    originalPlaylist.set(newPlaylist);
    playlist.set(newPlaylist);
    



}

export function shufflePlaylist() {
    let playlistValue;
    let currentIndexValue;
    let currentSongValue;

    playlist.subscribe(value => playlistValue = value)();
    currentIndex.subscribe(value => currentIndexValue = value)();
    currentSong.subscribe(value => currentSongValue = value)();

    let shuffledPlaylist = [...playlistValue];

    // 使用 Fisher-Yates 算法打乱播放列表
    for (let i = shuffledPlaylist.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [shuffledPlaylist[i], shuffledPlaylist[j]] = [shuffledPlaylist[j], shuffledPlaylist[i]];
    }

    const newIndex = shuffledPlaylist.findIndex(song => song.title === currentSongValue.title);


    playlist.set(shuffledPlaylist);
    currentIndex.set(newIndex);

}

export function restoreOriginalPlaylist() {
    let originalPlaylistValue;
    let currentSongValue;

    originalPlaylist.subscribe(value => originalPlaylistValue = value)();
    currentSong.subscribe(value => currentSongValue = value)();
    
    
    playlist.set([...originalPlaylistValue]);  // 恢复为原始播放列表

    const newIndex = originalPlaylistValue.findIndex(song => song.title === currentSongValue.title);

    // 更新当前播放歌曲的新索引
    currentIndex.set(newIndex);
}

export function playSongAtIndex(index) {
    initAudio(); // 确保 audio 已初始化

    let playlistValue;
    playlist.subscribe(value => {
        playlistValue = value;
    })();

    if (playlistValue && index >= 0 && index < playlistValue.length) {
        const song = playlistValue[index];
        currentIndex.set(index);
        playSong(song);
    } else {
        console.error("Invalid song index");
    }
}


export function playSong(song) {
    initAudio(); // 确保 audio 已初始化

    currentSong.set(song);
    songTitle.set(song.title || "song name");
    artist.set(song.artist || "artist");
    cover.set(song.cover || "/images/image.png");
    lyrics.set(song.lyrics || "No lyrics available");
    audio.src = song.url;

    // 设置是否单曲循环
    let loopModeValue;
    loopMode.subscribe(value => {
        loopModeValue = value;
    })();

    audio.loop = loopModeValue === 2; // 如果是单曲循环模式，则设置 audio.loop

    audio.play().catch((error) => {
        console.error('Error playing audio:', error);
    });
}

export function playPrevious() {
    let indexValue;
    let playlistValue;
    let shuffleValue;
    let loopModeValue;

    currentIndex.subscribe(value => {
        indexValue = value;
    })();
    playlist.subscribe(value => {
        playlistValue = value;
    })();
    shuffle.subscribe(value => {
        shuffleValue = value;
    })();
    loopMode.subscribe(value => {
        loopModeValue = value;
    })();

    if (loopModeValue === 2) {
        // 单曲循环，重新播放当前歌曲
        playSongAtIndex(indexValue);
    } else {
        if (indexValue > 0) {
            playSongAtIndex(indexValue - 1);
        } else if (loopModeValue === 1) {
            playSongAtIndex(playlistValue.length - 1);
        }
    }
}


export function playNext() {
    let indexValue;
    let playlistValue;
    let shuffleValue;
    let loopModeValue;

    currentIndex.subscribe(value => {
        indexValue = value;
    })();
    playlist.subscribe(value => {
        playlistValue = value;
    })();
    shuffle.subscribe(value => {
        shuffleValue = value;
    })();
    loopMode.subscribe(value => {
        loopModeValue = value;
    })();

    if (loopModeValue === 2) {
        // 单曲循环，重新播放当前歌曲
        playSongAtIndex(indexValue);
    } else {
        if (indexValue < playlistValue.length - 1) {
            playSongAtIndex(indexValue + 1);
        } else if (loopModeValue === 1) {
            playSongAtIndex(0);  // 列表循环，回到最后一首
        }
    }
}




<script>
  import { onMount } from 'svelte';
  import { page } from '$app/stores';
  import axios from 'axios';

  let searchQuery = '';
  let searchResults = [];
  let audioElement;
  import { createPlaylist, playMusic, pauseMusic, addToPlaylist } from '$lib/components/audioController.js';

  onMount(() => {
      audioElement = new Audio();
  });

  // Watch the URL for changes to query parameters
  $: {
      searchQuery = $page.url.searchParams.get('query') || '';
  }

  // Fetch search results when the searchQuery changes
  $: if (searchQuery) {
      fetchSearchResults();
  }

  async function fetchSearchResults() {
      try {
          const response = await axios.get(`http://127.0.0.1:8000/api/search_songs/`, {
              params: { query: searchQuery },
          });
          searchResults = response.data;
          console.log(searchResults)
      } catch (error) {
          console.error('Error fetching search results:', error);
      }
  }

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
          audioElement.play();
          console.log('Loaded music:', fileName);
      } catch (error) {
          console.error('Error loading music:', error);
      }
  }

  function openAddToPlaylistModal(song) {
      console.log('Add to playlist:', song);
  }

  function playFromAnywhere(fileName) {
        playMusic(fileName);  // Play the specified music file
    }
</script>

<h1>Search Results</h1>
<p>Results for: {searchQuery}</p>

{#if searchResults.length > 0}
  <div class="song-list">
      <h2>Tracks</h2>
      <ul>
          {#each searchResults as song, index}
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
                          <i class="fas fa-plus"></i>
                      </button>
                  </div>
              </li>
          {/each}
      </ul>
  </div>

  <div class="song-footer">
      <p>Found {searchResults.length} Songs</p>
  </div>
{:else if searchQuery}
  <p>No results found for "{searchQuery}"</p>
{:else}
  <p>Enter a query to search for songs.</p>
{/if}

<style>
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

  .song-footer {
      margin-top: 1.5rem;
      color: #999;
      text-align: center;
  }

  .add-playlist-button {
      background: none;
      border: none;
      cursor: pointer;
  }

  .add-playlist-button i {
      color: #ff3b3b;
  }
</style>

<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css" />
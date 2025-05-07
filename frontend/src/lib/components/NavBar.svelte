<script>
    import { user } from '$lib/stores/userStore';

    let menuItems = [
        { icon: "fas fa-home", label: "Home", path: "/" },
        { icon: "fas fa-star", label: "New", path: "/new" },
        { icon: "fas fa-podcast", label: "Radio", path: "/radio" }
    ];

    let top15Playlist = [
        'Song 1', 'Song 2', 'Song 3', 'Song 4', 'Song 5',
        'Song 6', 'Song 7', 'Song 8', 'Song 9', 'Song 10',
        'Song 11', 'Song 12', 'Song 13', 'Song 14', 'Song 15'
    ];

    let userPlaylists = [
        'Favorite Songs', 'Mix 1', 'Mix 2', 'Mix 3'
    ];

    let isPlaylistOpen = false;
    let isUserPlaylistOpen = false;
    // let isLoggedIn = false; // simulate login
    // $: isLoggedIn = $user.isLoggedIn;

    function addPlaylist() {
        console.log("submit")
    }
</script>

<nav class="sidebar">
    <!-- Logo -->
    <div class="logo-section">
        <div class="logo">
            <a href="/">
                <i class="fas fa-music"></i> Music
            </a>
        </div>
    </div>

    <!-- menu group -->
    <div class="menu-section">
        <ul class="menu-group">
            {#each menuItems as item}
                <li>
                    <a href={item.path} class="menu-link">
                        <i class="{item.icon}"></i>
                        <span class="menu-label">{item.label}</span>
                    </a>
                </li>
            {/each}
        </ul>
    </div>

    <!-- Top 15 Playlist -->
    <div class="playlist-section">
        <!-- use div element and add keyboard event and ARIA -->
        <div 
            class="playlist-header" 
            role="button" 
            tabindex="0" 
            aria-expanded={isPlaylistOpen} 
            aria-controls="top15-playlist"
            on:click={() => isPlaylistOpen = !isPlaylistOpen}
            on:keydown={(e) => e.key === 'Enter' || e.key === ' ' ? isPlaylistOpen = !isPlaylistOpen : null}
        >
            <i class="fas fa-list"></i> Top 15 Playlist 
            <i class="fas fa-chevron-down" style="float: right;"></i>
        </div>
        
        {#if isPlaylistOpen}
            <ul id="top15-playlist" class="playlist" aria-labelledby="top15-playlist">
                {#each top15Playlist as song}
                    <li>{song}</li>
                {/each}
            </ul>
        {/if}
    </div>
    

    <!-- user's playlist (only show after sign in) -->
    
    <div class="user-playlist-section">
        <!-- use div element and add keyboard event and ARIA  -->
         <button on:click={addPlaylist}>
            New Playlist
         </button>
        <div 
            class="playlist-header"
            role="button"
            tabindex="0"
            aria-expanded={isUserPlaylistOpen} 
            aria-controls="user-playlist"
            on:click={() => isUserPlaylistOpen = !isUserPlaylistOpen}
            on:keydown={(e) => e.key === 'Enter' || e.key === ' ' ? isUserPlaylistOpen = !isUserPlaylistOpen : null}
        >
            <i class="fas fa-music"></i> My Playlists
            <i class="fas fa-chevron-down" style="float: right;"></i>
        </div>
        
        {#if isUserPlaylistOpen}
            <ul id="user-playlist" class="playlist" aria-labelledby="user-playlist">
                {#each userPlaylists as playlist}
                    <li>{playlist}</li>
                {/each}
            </ul>
        {/if}
    </div>
    

</nav>

<style>
    .sidebar {
        display: flex;
        flex-direction: column;
        height: calc(100vh - 3rem);
        overflow-y: auto; /* for vertical scrolling */
        background-color: #f9f9f9;
    }

    .logo-section {
        padding: 1rem;
        background-color: inherit;
    }

    .logo {
        font-size: 1.5rem;
        font-weight: bold;
    }

    .menu-section, .playlist-section, .user-playlist-section {
        padding: 1rem;
        background-color: inherit;
    }

    .menu-group, .playlist {
        list-style: none;
        padding: 0;
        margin: 0;
    }

    li {
        display: flex;
        align-items: center;
        padding: 0.75rem;
        cursor: pointer;
        transition: background-color 0.3s;
    }

    li:hover {
        background-color: #dcdcdc;
    }
    .menu-label {
        margin-left: 0.75rem;
        color: #333;
    }
    .menu-link {
        text-decoration: none;
    }

    .playlist-header {
        cursor: pointer;
        padding: 0.75rem;
        background-color: #ddd;
        margin-bottom: 0.5rem;
        border-radius: 5px;
    }

    .playlist-header:hover {
        background-color: #ccc;
    }

    /* 图标样式 */
    i {
        margin-right: 0.75rem;
    }
</style>


<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css" />

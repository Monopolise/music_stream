<script>
    import NavBar from '$lib/components/NavBar.svelte';
    import SearchBar from '$lib/components/SearchBar.svelte';
    import PlaybackControl from '$lib/components/PlaybackControl.svelte';
    import Login from '$lib/components/Login.svelte';
    import MusicPlayer from '$lib/components/MusicPlayer.svelte';
    let isSidebarOpen = true; 
    let isMobile = false;
    let isPortrait = false;

    // Detect window width changes and respond
    function handleResize() {
        const width = window.innerWidth;
        const height = window.innerHeight;
        if (window.innerWidth <= 768) {
            isMobile = true;
            isSidebarOpen = false; // The sidebar is hidden by default on narrow screens
            isPortrait = height > width;
        } else {
            isMobile = false;
            isSidebarOpen = true; // Show sidebar by default in widescreen
            isPortrait = false;
        }
    }

    // observe the window size
    import { onMount } from 'svelte';
    onMount(() => {
        window.addEventListener('resize', handleResize);
        handleResize(); // Called once at initialization to determine the layout
        return () => window.removeEventListener('resize', handleResize);
    });
</script>

<div class="app">
    <button class="menu-button" on:click={() => isSidebarOpen = !isSidebarOpen} class:hidden={!isMobile}>
        <i class="fas fa-bars"></i>
    </button>

    <!-- left navigation  -->
    <aside class="sidebar" class:is-hidden={!isSidebarOpen && isMobile} class:is-mobile={isMobile} class:is-portrait={isPortrait}>
        <NavBar />
    </aside>

    <!-- main content -->
    <main class="main-content" class:full-width={!isSidebarOpen && isMobile}>
        <SearchBar />
        <Login/>
        <slot /> <!-- page content -->
    </main>

    <!-- bottom playback control -->
    <div class="playback-control">
        <MusicPlayer/>
    </div>
</div>

<style>
    :global(html), :global(body) {
        margin: 0;
        padding: 0;
        overflow-x: hidden; 
        width: 100%;
        height: 100%;
    }

    .playback-control {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #fff; /* or any background color you want */
        padding: 10px; /* Optional: add padding */
        box-shadow: 0 -2px 5px rgba(0, 0, 0, 0.1); /* Optional: add a shadow for better visibility */
        z-index: 1000; /* Ensure it is above other elements */
    }

    .app {
        display: flex;
        flex-direction: column;
        min-height: 100vh;
        width: 100%;
    }

    .sidebar {
        flex: 0 0 20%;
        height: 100vh; 
        box-sizing: border-box;
        position: fixed;
        top: 0;
        left: 0;
        background-color: #f4f4f4;
        z-index: 999;
        width: 15rem;
        transition: transform 0.3s ease-in-out;
    }

    .sidebar.is-mobile {
        top: 60px;
        height: calc(100vh - 50px);
    }

    .sidebar.is-hidden {
        transform: translateX(-100%); 
    }

    .sidebar.is-portrait {
        width: 100%;
        max-width: none; 
        height: auto;
    }

    .main-content {
        flex: 1;
        margin-left: 15rem;
        padding-top: 50px; 
        display: flex;
        flex-direction: column;
        width: calc(100% - 15rem);
        overflow-y: auto;
        transition: margin-left 0.3s ease-in-out;
    }

    .main-content.full-width {
        margin-left: 0; 
        width: 100%; 
    }

    .menu-button {
        position: fixed;
        top: 15px;
        left: 10px;
        background: none;
        border: none;
        font-size: 30px;
        cursor: pointer;
        z-index: 1000;
        display: none; 
    }

    .hidden {
        display: none;
    }

    
    @media (max-width: 768px) {
        .sidebar {
            position: fixed;
            top: 0;
            left: 0;
            height: 100vh;
            transform: translateX(-100%);
        }

        .sidebar.is-hidden {
            transform: translateX(-100%);
        }

        .sidebar:not(.is-hidden) {
            transform: translateX(0);
        }

        
        .menu-button {
            display: block;
        }

        
        .main-content.full-width {
            width: 100%;
        }
    }
</style>

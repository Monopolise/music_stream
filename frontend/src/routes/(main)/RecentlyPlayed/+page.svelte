<script>
    import MusicList from '$lib/components/MusicList.svelte';
    // simulate
    const recentlyPlayed = [
        {id:12, cover: '/images/image12.png', title: 'Hai Yorokonde - Single', artist: 'Kocchi No Kento' },
        {id:13, cover: '/images/image13.png', title: '光年之外', artist: 'G.E.M.' },
        {id:14, cover: '/images/image14.png', title: 'RAMMSTEIN', artist: 'Rammstein' },
        {id:15, cover: '/images/image15.png', title: 'New Divide ', artist: 'LINKIN PARK' },
        {id:16, cover: '/images/image16.png', title: 'Cause and Effect (Deluxe) ', artist: 'Keane' },
        {id:17, cover: '/images/image17.png', title: 'American Idiot ', artist: 'Green Day' },
        {id:18, cover: '/images/image18.png', title: 'Save Rock and Roll', artist: 'Fall Out Boy' },
        {id:19, cover: '/images/image19.png', title: 'Shikiuta Summer', artist: 'BENI' },
        {id:20, cover: '/images/image20.png', title: 'Wrong World - Single', artist: 'TOGENASHITOGEARI' },
        {id:21, cover: '/images/image21.png', title: 'replica', artist: 'VAUNDY' },
        {id:22, cover: '/images/image22.png', title: 'visions', artist: 'milet' },
    ];
</script>

<div class="page-content">
    <h2>Recently Played </h2>
    <div class="album-grid">
        <!-- Traverse and render virtual albums -->
        {#each recentlyPlayed as album}
            <MusicList id={album.id} cover={album.cover} title={album.title} artist={album.artist} />
        {/each}
    </div>
</div>

<style>
    h2 {
        font-size: 2rem; /* Increase font size */
        font-weight: bold; /* Bold font */
        color: #333; /* font color */
        margin-bottom: 1.5rem; /* bottom gap of title */
    }
    .page-content {
        padding: 1rem;
        flex: 1;
        display: flex;
        flex-direction: column;
        padding-bottom: 5rem;
    }
    /* Use a grid layout to present album cover and song information */
    .album-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
        gap: 2rem;
        justify-items: center;
        align-items: center;
    }
    
    @media (max-width: 768px) {
        .album-grid {
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
        }
    }

    @media (min-width: 1600px) {
        .album-grid {
            grid-template-columns: repeat(6, minmax(200px, 1fr)); /* 最大列数为4 */
        }
    }
</style>
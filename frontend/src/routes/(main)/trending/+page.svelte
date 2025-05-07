<script>
    import MusicList from '$lib/components/MusicList.svelte';
    // simulate
    const trending = [
        {id:23, cover: '/images/image23.png', title: '爱', artist: 'The Little Tigers' },
        {id:24, cover: '/images/image24.png', title: 'Hot Space (Deluxe Edition)', artist: 'Queen' },
        {id:25, cover: '/images/image25.png', title: 'One Love', artist: 'Blue' },
        {id:26, cover: '/images/image26.png', title: '命运派对', artist: 'Beyond' },
        {id:27, cover: '/images/image27.png', title: 'Hotel California', artist: 'Eagles' },
        {id:28, cover: '/images/image28.png', title: '21st Century Breakdown (Deluxe Edition)', artist: 'Green Days' },
        {id:29, cover: '/images/image29.png', title: 'Sleepless Nights', artist: 'Aimer' },
        {id:30, cover: '/images/image30.png', title: 'Into the Sky EP', artist: 'SawanoHiroyuki[nZk]' },
    ];
</script>

<div class="page-content">
    <h2>Trending </h2>
    <div class="album-grid">
        <!-- Traverse and render virtual albums -->
        {#each trending as album}
            <MusicList id={album.id} cover={album.cover} title={album.title} artist={album.artist} />
        {/each}
    </div>
</div>

<style>
    h2 {
        font-size: 2rem;
        font-weight: bold; 
        color: #333; 
        margin-bottom: 1.5rem; 
    }
    .page-content {
        padding: 1rem;
        flex: 1;
        display: flex;
        flex-direction: column;
        padding-bottom: 5rem;
    }
    
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
<script>
    import MusicList from '$lib/components/MusicList.svelte';
    import { onMount } from 'svelte';

    // simulate
    const recommended = [
        {id:1, cover: '/images/image30.png', title: 'Greatest Hits', artist: 'test' },
        {id:2, cover: '/images/image1.png', title: 'Smooth Jazz', artist: 'Imagine Dragons' },
        {id:3, cover: '/images/image2.png', title: 'Classic Rock Collection', artist: 'Bryan Adams' },
        {id:4, cover: '/images/image3.png', title: 'Electronic Beats', artist: 'BENI' },
        {id:5, cover: '/images/3.png', title: 'Acoustic Chill', artist: 'kessoku band' },
        {id:6, cover: '/images/image5.png', title: 'Pop Hits 2021', artist: 'League of Legends Music, PVRIS' },
        {id:7, cover: '/images/image6.png', title: 'Jazz Vibes', artist: 'Bertie Higgins' },
        {id:8, cover: '/images/image7.png', title: 'Indie Rock Essentials', artist: 'Ave Mujica' },
        {id:9, cover: '/images/image8.png', title: 'Hip Hop Legends', artist: '朴树' },
        {id:10, cover: '/images/image9.png', title: 'Classical Greats', artist: 'K/DA, (G)I-DLE, Wolftyla' },
        {id:11, cover: '/images/image11.png', title: 'Country Roads', artist: 'Beyond' },
    ];

    const recentlyPlayed = [
        {id:12, cover: '/images/image12.png', title: 'RnB Love Songs', artist: 'Kocchi No Kento' },
        {id:13, cover: '/images/image13.png', title: 'Heavy Metal Thunder', artist: 'G.E.M.' },
        {id:14, cover: '/images/image14.png', title: 'Chillwave Compilation', artist: 'Rammstein' },
        {id:15, cover: '/images/image15.png', title: 'Blues Classics', artist: 'LINKIN PARK' },
        {id:16, cover: '/images/image16.png', title: 'EDM Party Hits', artist: 'Keane' },
        {id:17, cover: '/images/image17.png', title: 'Reggae Rhythms', artist: 'Green Day' },
        {id:18, cover: '/images/image18.png', title: 'Soul Grooves', artist: 'Fall Out Boy' },
        {id:19, cover: '/images/image19.png', title: 'Folk Revival', artist: 'BENI' },
        {id:20, cover: '/images/image20.png', title: 'Punk Rock Anthems', artist: 'TOGENASHITOGEARI' },
        {id:21, cover: '/images/image21.png', title: 'Latin Fiesta', artist: 'VAUNDY' },
        {id:22, cover: '/images/image22.png', title: 'Ambient Soundscapes', artist: 'milet' },
    ];

    const trending = [
        {id:23, cover: '/images/image23.png', title: 'Descendants of the Sun, Pt. 1 (Original Television Soundtrack)', artist: 'The Little Tigers' },
        {id:24, cover: '/images/image24.png', title: 'Songs in the Key of Life', artist: 'Queen' },
        {id:25, cover: '/images/image25.png', title: 'Alive', artist: 'Blue' },
        {id:26, cover: '/images/image26.png', title: 'EASY LISTENING', artist: 'Beyond' },
        {id:27, cover: '/images/image27.png', title: 'THE GREAT LEAP', artist: 'Eagles' },
        {id:28, cover: '/images/image28.png', title: 'Black Tangerine', artist: 'Green Days' },
        {id:29, cover: '/images/image29.png', title: 'The Very Best of Sting & The Police', artist: 'Aimer' },
        {id:30, cover: '/images/image30.png', title: 'Daydream', artist: 'SawanoHiroyuki[nZk]' },
    ];

     // scrolling
    let recommendedRef, recentlyPlayedRef, trendingRef;
    let itemsPerPage = 1;

    function updateItemsPerPage(ref) {
        if (ref && ref.offsetWidth) {  // 确保 ref 已经被渲染并有 offsetWidth 属性
            const itemWidth = 200;
            const margin = 20;
            const containerWidth = ref.offsetWidth;
            itemsPerPage = Math.floor(containerWidth / (itemWidth + margin));
        }
    }

    onMount(() => {
        updateItemsPerPage(recommendedRef);
        updateItemsPerPage(recentlyPlayedRef);
        updateItemsPerPage(trendingRef);
        window.addEventListener('resize', () => {
            updateItemsPerPage(recommendedRef);
            updateItemsPerPage(recentlyPlayedRef);
            updateItemsPerPage(trendingRef);
        });
    });

    function scrollLeft(ref) {
        const scrollDistance = itemsPerPage * 220;
        ref.scrollBy({ left: -scrollDistance, behavior: 'smooth' });
    }

    function scrollRight(ref) {
        const scrollDistance = itemsPerPage * 220;
        ref.scrollBy({ left: scrollDistance, behavior: 'smooth' });
    }
</script>


<div class="page-content">
    <div class="section">
        <h2>Top Picks for You</h2>
        <div class="carousel-wrapper">
            <div class="button-container">
                <button class="carousel-button prev" on:click={() => scrollLeft(recommendedRef)}>
                    <i class="fas fa-chevron-left"></i>
                </button>
            </div>
            <div class="carousel-container">
                <div bind:this={recommendedRef} class="carousel-content">
                    {#each recommended as album}
                        <div class="carousel-item">
                            <MusicList id={album.id} cover={album.cover} title={album.title} artist={album.artist} />
                        </div>
                    {/each}
                </div>
            </div>
            <div class="button-container">
                <button class="carousel-button next" on:click={() => scrollRight(recommendedRef)}>
                    <i class="fas fa-chevron-right"></i>
                </button>
            </div>
        </div>
    </div>

    <div class="section">
        <a href="/RecentlyPlayed" class="carousel-link">
            <h2>Recently Played <span class="arrow">›</span></h2>
        </a>
        <div class="carousel-wrapper">
            <div class="button-container">
                <button class="carousel-button prev" on:click={() => scrollLeft(recentlyPlayedRef)}>
                    <i class="fas fa-chevron-left"></i>
                </button>
            </div>
            <div class="carousel-container">
                <div bind:this={recentlyPlayedRef} class="carousel-content">
                    {#each recentlyPlayed as album}
                        <div class="carousel-item">
                            <MusicList id={album.id} cover={album.cover} title={album.title} artist={album.artist} />
                        </div>
                    {/each}
                </div>
            </div>
            <div class="button-container">
                <button class="carousel-button next" on:click={() => scrollRight(recentlyPlayedRef)}>
                    <i class="fas fa-chevron-right"></i>
                </button>
            </div>
        </div>
        
    </div>

    <div class="section">
        <a href="/trending" class="carousel-link">
            <h2>Trending <span class="arrow">›</span></h2>
        </a>
        <div class="carousel-wrapper">
            <div class="button-container">
                <button class="carousel-button prev" on:click={() => scrollLeft(trendingRef)}>
                    <i class="fas fa-chevron-left"></i>
                </button>
            </div>
            <div class="carousel-container">
                <div bind:this={trendingRef} class="carousel-content">
                    {#each trending as album}
                        <div class="carousel-item">
                            <MusicList id={album.id} cover={album.cover} title={album.title} artist={album.artist} />
                        </div>
                    {/each}
                </div>
            </div>
            <div class="button-container">
                <button class="carousel-button next" on:click={() => scrollRight(trendingRef)}>
                    <i class="fas fa-chevron-right"></i>
                </button>
            </div>
        </div>
    </div>
</div>



<style>
    h2 {
        font-size: 2rem; /* 增大字体 */
        font-weight: bold; /* 加粗 */
        color: #333; /* 字体颜色 */
        margin-bottom: 1.5rem; /* 标题下方的间距 */
    }
    .page-content {
        padding: 2rem;
        flex: 1;
        display: flex;
        flex-direction: column;
        /* padding-bottom: 5rem; */
    }

    .section {
        margin-bottom: 3rem;
    }

    .carousel-wrapper {
        display: flex;
        align-items: center;
        position: relative;
        gap: 1rem;
    }


    .carousel-container {
        overflow: hidden;
        flex-grow: 1;
        flex-grow: 1;
        align-items: center;
    }

    .carousel-content {
        display: flex;
        gap:  2rem;
        overflow-x: auto;
        scroll-behavior: smooth;
        padding: 1rem;
        width: 100%;
        /* padding: 1rem 0; */
    }
    .carousel-item {
        min-width: 200px;
        flex: 0 0 20%;
        height:auto;
        padding: 0.5rem; /* inside padding */
        box-sizing: border-box;
    }
    .button-container {
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .carousel-button {
        background-color: inherit;
        color: rgb(174, 174, 174);
        border: none;
        font-size: 24px;
        cursor: pointer;
        z-index: 1;
        padding: 0.5rem;
    }


    .carousel-content::-webkit-scrollbar {
        display: none;
    }

    a.carousel-link {
        text-decoration: none;
        color: inherit;
        display: flex;
        align-items: center;
        gap: 0.3rem;
    }

    a.carousel-link:hover {
        cursor: pointer;
        color: #333;
    }
    .arrow {
        font-size: 1.5rem;
        color: #999; 
    }


    @media (max-width: 768px) {
        /* .album-grid {
            grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
        } */
        .carousel-item {
            min-width: 200px; /* 小屏幕时调整最小宽度 */
        }
    }
</style>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css" />
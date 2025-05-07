<script>
    import TrackInfo from '$lib/components/TrackInfo.svelte'; // 引入 TrackInfo 组件
    export let data;

    $: data = data;
    console.log(data?.message);
    console.log(data?.album_data?.tracks);
</script>

{#if data?.message?.includes("success")}
    <TrackInfo
        albumCover={data?.album_data?.cover_img_url || ""} 
        albumTitle={data?.album_data?.title || ""} 
        artistName={data?.album_data?.artist?.name || ""}
        releaseDate={data?.album_data?.release_date || ""}
        duration={data?.album_data?.duration || ""}
        songList={data?.album_data?.tracks?.map(track => ({
            title: track?.title || "",
            duration: track?.duration || "",
            url: track?.resource_link || "",
            lyrics: track?.lyrics || ""
        })) || []}
    />
{:else}
    <div>
        No Album Found
    </div>
{/if}

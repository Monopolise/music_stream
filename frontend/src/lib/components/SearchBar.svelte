<script>

    let query = '';

    function search() {
        console.log('Searching for:', query);
        // Implement search logic here
    }
</script>

<div class="search-bar">
    <input type="text" bind:value={query} placeholder="Search for music..." />
    <!-- <button on:click={search}>Search</button> -->
    <a href={`/search_result?query=${encodeURIComponent(query)}`} class="search-icon">
        <i class="fa fa-search"></i>
    </a>
</div>

<style>
    .search-bar {
        position: fixed;
        top: 10px;
        left: 50%;
        transform: translateX(-50%); /* Horizontal Center */
        z-index: 1000;

        display: flex;
        justify-content: center;
        align-items: center;
        
        padding: 0;
        background-color: transparent;

        margin: 0;
        line-height: 1;

        height:40px;
        width: 40%
    }
    input {
        padding: 0.5rem;
        font-size: 1rem;
        margin: 0 1rem 0 0;
        width: 75%;
    }
    .search-icon {
        cursor: pointer;
        padding: 0 10px;
        color: #e57373; 
    }

    .fa-search {
        font-size: 1.2rem;
    }

    .search-icon:hover {
        color: #00BFFF;
    }
</style>

<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css" />


<script>

</script>

<div class="admin-container flex flex-col">
    <div class="admin-title">
        Welcome to the Admin Panel
    </div>
    <div class="tool-grid grid grid-cols-4">
        <div class="link-container">
            <a href="/admin/new_track">add track</a>
        </div>
        <div class="link-container">
            <a href="/admin/new_album">add Album</a>
        </div>
        <div class="link-container">
            <a href="/admin/new_genre">add Genre</a>
        </div>
        <div class="link-container">
            <a href="/admin/new_artist">add Artist</a>
        </div>
        <div class="link-container">
            <a href="/admin/add_album_to_artist">add Album to Artist</a>
        </div>
        <div class="link-container">
            <a href="/admin/add_track_to_album">add Track to Album</a>
        </div>
        <div class="link-container">
            <a href="/admin/add_track_to_artist">add Track to Artist</a>
        </div>
        <div class="link-container">
            <a href="/admin/add_track_to_genre">add Track to Genre</a>
        </div>
    </div>
</div>

<style>
    .admin-container {
        justify-content: center;
        align-items: center;
        margin-top: 50px;
    }

    .admin-title {
        font-weight: 700;
        font-size: 35px;
        text-align: center;
    }

    .tool-grid {
        width: 1000px;
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 20px; /* Adjust gap between grid items */
    }

    .link-container {
        height: 100px;
        background-color: #bb6b6bb0;
        display: flex;
        justify-content: center;
        align-items: center;
        border-radius: 8px; /* Rounded corners */
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* Subtle shadow */
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .link-container:hover {
        transform: scale(1.05); /* Slight zoom on hover */
        box-shadow: 0 6px 10px rgba(0, 0, 0, 0.15); /* Increased shadow on hover */
    }

    .link-container:active {
        transform: scale(0.98); /* Shrink slightly on click */
    }

    .tool-grid a {
        color: black;
        text-decoration: none;
        font-weight: 500;
        font-size: 18px;
        text-transform: capitalize;
    }
</style>
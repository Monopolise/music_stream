<script>
    import { enhance } from '$app/forms';

    export let form;
    export let data;

    let currentContent = "Add Content";
    const changeContent = (content) => {
        currentContent = content;
    };

    // Ensure fallback to data's CSRF token if form is undefined
    $: csrfToken = form?.csrfToken || data?.csrfToken || ''; // Fallback to empty string if both are undefined
</script>

<div class="admin-panel">
    <!-- Dynamic Content Area -->
    <div class="flex flex-col">
        <div class="form-group">
            <div class="input-title">
                Add Track
            </div>
            <form method="POST" action="?/addTrack" enctype="multipart/form-data" use:enhance class="flex flex-col input-group">
                <!-- Dynamically assign CSRF token, if available -->
                {#if csrfToken}
                    <input type="hidden" name="csrfmiddlewaretoken" value={csrfToken} />
                {/if}
                
                <input type="text" name="title" placeholder="title" required />
                <input type="text" name="duration" placeholder="duration in seconds" required />
                <input type="file" name="file" placeholder="in seconds" required />
                <input type="text" name="releaseDate" placeholder="releaseDate" required />
                <input type="text" name="lyrics" placeholder="lyrics" required />
                
                <button type="submit" class="submit-button">Submit</button>

                {#if form?.error}
                    <p style="color: red;">{form.error}</p>
                {/if}
            </form>
        </div>
    </div>
</div>

<style>
    .admin-panel {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh; /* Ensures the panel takes the full viewport height */
    }

    .flex.flex-col {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: auto;
    }

    .form-group {
        width: 500px;
        margin-bottom: 20px;
        text-align: center; /* Center text in the form group */
    }

    .input-title {
        font-size: 25px;
        font-weight: 700;
        margin-bottom: 10px;
    }

    .input-group {
        gap: 10px;
        display: flex;
        flex-direction: column;
    }

    .input-group input {
        width: 100%; /* Make the inputs take full width */
        padding: 10px;
        font-size: 16px;
        border: 1px solid #ccc;
        border-radius: 5px;
    }

    .submit-button {
        border-radius: 5px;
        width: 100px; /* Increased width for better alignment */
        border-width: 1px;
        border-style: solid;
        border-color: black;
        padding: 5px 10px;
        align-self: center; /* Center the submit button */
        background-color: white;
        color: black;
        cursor: pointer; /* Changes cursor to pointer when hovering over button */
        transition: background-color 0.3s ease, color 0.3s ease; /* Smooth transition effect */
    }

    /* Hover effect for the submit button */
    .submit-button:hover {
        background-color: rgb(121, 253, 217); /* Change background color on hover */
        color: rgb(0, 0, 0); /* Change text color on hover */
        border-color: black; /* Keep the border black */
    }
</style>
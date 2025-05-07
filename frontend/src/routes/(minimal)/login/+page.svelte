<script>
    import { enhance } from '$app/forms';
    import QuoteOfTheDay from '$lib/components/QuoteOfTheDay.svelte';

    export let form;
    export let data;

    // Ensure fallback to data's CSRF token if form is undefined
    $: csrfToken = form?.csrfToken || data?.csrfToken || ''; // Fallback to empty string if both are undefined
</script>

<!-- Create a container that splits the page into two sections -->
<div class="page-container">
    <!-- Left section: Title and Login Form -->
    <div class="left-section">
        <!-- Website Title -->
        <h1 class="site-title">MusicFlow</h1> <!-- 你可以根据需要修改这个网站的名字 -->
        <!-- Login Form -->
        <form method="POST" action="?/login" use:enhance class="login-group flex flex-col">
            <!-- Dynamically assign CSRF token, if available -->
            {#if csrfToken}
                <input type="hidden" name="csrfmiddlewaretoken" value={csrfToken} />
            {/if}

            <h2 class="login-title">Login to Your Account</h2>

            <input type="text" name="username" placeholder="Username" class="input-field" required />
            <input type="password" name="password" placeholder="Password" class="input-field" required />
            <input type="text" name="mfa_code" placeholder="MFA Code (if enabled)" class="input-field" />

            <button type="submit" class="submit-button">Login</button>

            {#if form?.error}
                <p class="error-message">{form.error}</p>
            {/if}

            <div class="extra-links">
                <a href="/register" class="register-link">Don't have an account? Register here</a>
            </div>
        </form>
        <QuoteOfTheDay/>
    </div>

    <!-- Right section: Website introduction -->
    <div class="right-section">
        <div class="introduction">
            <h2>Welcome to MusicFlow!</h2>
            <p>MusicFlow is your ultimate music streaming platform. Discover new music, create playlists, and share your favorite tracks with friends. Join us and start vibing to your favorite tunes now!</p>
        </div>
    </div>
</div>

<style>
    /* Page layout */
    .page-container {
        display: flex;
        height: 100vh;
    }

    .left-section {
        flex: 1;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        background-color: #f5f5f5;
        padding: 20px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }

    .right-section {
        flex: 1;
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: #fff;
        padding: 50px;
    }

    .site-title {
        position: absolute;
        top: 20px;
        left: 20px;
        font-size: 2em;
        font-weight: bold;
        color: #333;
    }

    /* Login form styles */
    .login-group {
        width: 350px;
        padding: 20px;
        background-color: #fff;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        border-radius: 10px;
        gap: 20px;
        text-align: center;
    }

    .login-title {
        font-size: 1.5em;
        font-weight: bold;
        color: #333;
        margin-bottom: 20px;
    }

    .input-field {
        padding: 10px;
        font-size: 1em;
        border: 1px solid #ccc;
        border-radius: 5px;
        transition: border-color 0.3s;
    }

    .input-field:focus {
        border-color: #007BFF;
        outline: none;
    }

    .submit-button {
        padding: 12px;
        font-size: 1em;
        color: #fff;
        background-color: #007BFF;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        transition: background-color 0.3s;
    }

    .submit-button:hover {
        background-color: #0056b3;
    }

    .error-message {
        color: red;
        font-weight: bold;
        margin-top: -10px;
    }

    .extra-links {
        margin-top: 10px;
    }

    .register-link {
        text-decoration: none;
        color: #007BFF;
        transition: color 0.3s;
    }

    .register-link:hover {
        color: #0056b3;
    }

    /* Introduction section styles */
    .introduction {
        max-width: 500px;
        text-align: left;
    }

    .introduction h2 {
        font-size: 2em;
        margin-bottom: 10px;
    }

    .introduction p {
        font-size: 1.1em;
        color: #555;
        line-height: 1.5;
    }
</style>
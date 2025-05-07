<script>
    import { enhance } from '$app/forms';
    let isSubmitting = false;  // Flag to track if the form is being submitted

    export let form;
    export let data;

    // Ensure fallback to data's CSRF token if form is undefined
    $: csrfToken = form?.csrfToken || data?.csrfToken || ''; // Fallback to empty string if both are undefined

    // This function will be triggered when the form is enhanced and submission starts
    const handleSubmit = async (event) => {
        isSubmitting = true;
    };

    const handleSuccess = () => {
        isSubmitting = false;
    };

    const handleError = () => {
        isSubmitting = false;
    };
</script>

<!-- Create a container that splits the page into two sections -->
<div class="page-container">
    <!-- Left section: Title and Registration Form -->
    <div class="left-section">
        <!-- Website Title -->
        <h1 class="site-title">MusicFlow</h1> <!-- 网站标题保持不变 -->

        <!-- Registration Form -->
        <form method="POST" action="?/register" use:enhance class="input-group flex flex-col">
            <!-- Dynamically assign CSRF token, if available -->
            {#if csrfToken}
                <input type="hidden" name="csrfmiddlewaretoken" value={csrfToken} />
            {/if}

            <h2 class="form-title">Create a New Account</h2>

            <input type="email" name="username" placeholder="example@example.com" required />
            <input type="password" name="password" placeholder="Password" required />
            <input type="text" name="name" placeholder="John Connor" required />
            <input type="text" name="displayName" placeholder="Obiwan" required />
            
            <!-- Disable the button if the form is being submitted -->
            <button type="submit" disabled={isSubmitting}>Register</button>

            {#if form?.error}
                <p style="color: red;">{form.error}</p>
            {/if}

            <a href="/login">Already have an account? Login</a>
        </form>
    </div>

    <!-- Right section: Additional information about registration -->
    <div class="right-section">
        <div class="introduction">
            <h2>Join MusicFlow Today!</h2>
            <p>Create an account and explore our vast music library. With personalized playlists, easy sharing, and a seamless music experience, MusicFlow offers everything you need to elevate your music listening. Sign up now and start your musical journey!</p>
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

    /* Form styles */
    .input-group {
        width: 350px;
        padding: 20px;
        background-color: #fff;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        border-radius: 10px;
        gap: 20px;
        text-align: center;
    }

    .form-title {
        font-size: 1.5em;
        font-weight: bold;
        color: #333;
        margin-bottom: 20px;
    }

    input {
        padding: 10px;
        font-size: 1em;
        border: 1px solid #ccc;
        border-radius: 5px;
        transition: border-color 0.3s;
    }

    input:focus {
        border-color: #007BFF;
        outline: none;
    }

    button {
        padding: 12px;
        font-size: 1em;
        color: #fff;
        background-color: #007BFF;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        transition: background-color 0.3s;
    }

    button:hover {
        background-color: #0056b3;
    }

    button:disabled {
        background-color: #6c757d;
        color: #ccc;
        cursor: not-allowed;
        opacity: 0.6;
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
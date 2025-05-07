<script>
    import { onMount, onDestroy } from 'svelte';
    import { user } from '$lib/stores/userStore';
    import { goto, invalidateAll } from '$app/navigation';

    let isMenuVisible = false;

    function logout() {
        console.log('logout');
        user.update(current => ({ ...current, isLoggedIn: false }));
        isMenuVisible = false; // Close the menu

        // Redirect to /logout and invalidate session data
        goto('/logout').then(() => {
            // Invalidate any relevant data that needs to be refreshed
            invalidateAll();
        });
    }

    function toggleUserMenu() {
        isMenuVisible = !isMenuVisible;
    }

    function hideUserMenu(event) {
        if (
            isMenuVisible &&
            event.target.closest('.user-menu') === null &&
            event.target.closest('.user-icon-button') === null
        ) {
            isMenuVisible = false;
        }
    }

    function navigate(path) {
        goto(path);
        isMenuVisible = false; // 关闭菜单
    }

    onMount(() => {
        if (typeof window !== 'undefined') {
            document.addEventListener('click', hideUserMenu);
        }
    });

    onDestroy(() => {
        if (typeof window !== 'undefined') {
            document.removeEventListener('click', hideUserMenu);
        }
    });
</script>

<div class="login-component">
    <!-- 显示用户图标 -->
    <button class="user-icon-button" on:click={toggleUserMenu} title="User Menu">
        <img src="/images/user-icon.png" alt="User Icon" class="user-icon" />
    </button>

    {#if isMenuVisible}
        <div class="user-menu">
            <button class="menu-button" on:click={() => navigate('/settings')}>Settings</button>
            <button class="menu-button" on:click={logout}>Sign Out</button>
            <button class="menu-button" on:click={() => navigate('/profile')}>User Profile</button>
        </div>
    {/if}
</div>

<style>
    .user-icon-button {
        position: fixed;
        top: 20px;
        right: 20px;
        cursor: pointer;
        background-color: transparent;
        border: none;
    }

    .user-icon {
        width: 40px;
        height: 40px;
        border-radius: 50%;
    }

    .user-menu {
        position: fixed;
        top: 70px;
        right: 20px;
        background-color: black;
        color: white;
        border-radius: 5px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        padding: 10px;
        z-index: 1000;
    }

    .menu-button {
        background-color: transparent;
        color: white;
        border: none;
        padding: 10px;
        cursor: pointer;
        width: 100%;
        text-align: left;
    }

    .menu-button:hover {
        background-color: rgba(255, 255, 255, 0.1);
    }

    .login-component {
        position: fixed;
        top: 10px;
        right: 20px;
        z-index: 1000;
        display: flex;
        align-items: center;
        justify-content: flex-end;
        margin: 0;
        line-height: 1; 
        height: 40px;
    }
</style>

// userStore.js
import { writable } from 'svelte/store';

export const user = writable({
    isLoggedIn: false,
});

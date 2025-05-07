// src/lib/stores/favoritesStore.js
import { writable } from 'svelte/store';

// 初始化一个空的喜爱歌曲列表
export const favorites = writable([]);

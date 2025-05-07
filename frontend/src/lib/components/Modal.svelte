<!-- src/lib/components/Modal.svelte -->
<script>
    import { createEventDispatcher } from 'svelte';

    const dispatch = createEventDispatcher();

    function handleOverlayClick(event) {
        if (event.target === event.currentTarget) {
            dispatch('close');
        }
    }
</script>

<div class="modal-overlay" on:click={handleOverlayClick}>
    <div class="modal-content">
        <slot></slot>
    </div>
</div>

<style>
    .modal-overlay {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 1000;
    }

    .modal-content {
        background: white;
        padding: 2rem;
        border-radius: 8px;
        width: 400px;
        max-width: 90%;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
</style>

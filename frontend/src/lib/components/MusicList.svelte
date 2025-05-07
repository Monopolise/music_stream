<script>
    import { goto } from '$app/navigation';
    export let id; 

    export let cover = '/images/image.png';
    export let title = 'Music Title';
    export let artist = 'Artist Name';
</script>

<a 
  class="music-container" 
  tabindex="0" 
  href={`/album/${title}`}
>
  <div class="music-info">
    <img src={cover} alt={title} />
    <div class="details">
      <h3>{title}</h3>
      <p>{artist}</p>
    </div>
  </div>
</a>

<style>
    .music-container {
        width: 100%; /* container got 100% width of parent element */
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 0.5rem; /* padding inside container */
        background-color: transparent; 
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* shadow for container */
        border-radius: 10px; /* border radius of container */
        transition: transform 0.2s;
        /* padding: 1rem; */
    }

    .music-container:hover {
        transform: translateY(-5px); /* Floating up effect when the mouse is hovering */
        cursor: pointer;
    }

    .music-info {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        width: 100%;
    }
    .details {
        max-width: 100%; /* limit max width as container width */
        width: 100%; 
    }
    .music-info img {
        width: 100%;
        height: auto;
        max-width: 500px;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    .music-info h3{
        margin-top: 0.5rem;
        font-size: 1.2rem;
        color: #333;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .music-info p{
        margin-top: 0.2rem;
        font-size: 1rem;
        color: #777;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
</style>

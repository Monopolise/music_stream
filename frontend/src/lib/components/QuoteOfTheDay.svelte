<script>
    import { onMount } from "svelte";
    let quote = "Loading...";
    let author = "";
  
    // Function to fetch the quote of the day
    async function fetchQuote() {
      try {
        const response = await fetch("http://api.quotable.io/random");
        const data = await response.json();
        quote = data.content;
        author = data.author;
      } catch (error) {
        quote = "Could not fetch quote. Please try again later.";
      }
    }
  
    // Fetch the quote when the component mounts
    onMount(fetchQuote);
  </script>
  
  <div class="login-container">
    <div class="quote-of-the-day">
      <p>"{quote}"</p>
      {#if author}
        <p>— {author}</p>
      {/if}
    </div>
  </div>
  
  <style>
    .quote-of-the-day {
      margin-top: 20px;
      font-style: italic;
      color: #555;
    }
  </style>
  
<script lang="ts">
	import type { PageData } from "./$types";

    export let data: PageData;
</script>

<div class="wrapper">
    <h3>Original Abstract Oil Paintings on Canvas and Prints</h3>
    <div class="masonry-layout">
        {#await data.products}
        
        {:then products} 
            {#each products as product}
                <div class="masonry-item">
                    {#if product.imageUrl}
                        <img src={product.imageUrl} alt={product.title} />
                    {/if}
                </div>
            {/each}
        {:catch error}
            <p style="color: red">{error.message}</p>
        {/await}
    </div>
</div>

<style>
    .wrapper {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;
    }

    .masonry-layout {
        column-count: 4; /* Adjust the number of columns based on your design */
        column-gap: 1rem; /* Space between columns */
        width: 100%; /* Full width of the container */
    }

    .masonry-item {
        break-inside: avoid; /* Prevent items from splitting across columns */
        margin-bottom: 1rem; /* Space between items */
        padding: 1rem; /* Padding inside items */
    }

    img {
        max-width: 225px;
        object-fit: contain;
    }
</style>
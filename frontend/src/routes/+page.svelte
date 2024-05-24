<script lang="ts">
    import { onMount } from "svelte";
    let products: any[] = [];

    onMount(async () => {
        const response = await fetch(`http://127.0.0.1:8000/products`);

        if (response.status === 200) {
            const responseData = await response.json();
            products = responseData;
        } else {
            console.log("Error retrieving products.");
        }
    });
</script>

<h3>Original Abstract Oil Paintings on Canvas and Prints</h3>

<div class="wrapper">
    {#each products as product}
        <div>
            {#if product.imageUrl}
                <img src={product.imageUrl} alt={product.title} />
            {/if}
        </div>
    {/each}
</div>


<style>
    .wrapper {
        display: flex;
        flex-direction: column;
    }

    img {
        max-width: 400px;
        max-height: 400px;
    }
</style>
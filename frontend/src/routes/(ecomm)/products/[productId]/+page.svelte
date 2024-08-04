<script lang="ts">
	import type { PageData } from "./$types";
    import PayPal from "$lib/components/PayPal.svelte";

    export let data: PageData;
</script>

<div class="wrapper">
    {#await data.product}
        <p>Loading product...</p>
    {:then product} 
        <img src="{product.images[0]}" alt={product.title} />
        <div class="row">
            <div class="column" style="flex: 3;">
                <h1>{product.title}</h1>
                <p>{product.description}</p>
            </div>
            <div class="column" style="flex: 2;">
                <div>
                    <div>
                        ${product.price}
                    </div>
                    <div>
                        + FREE shipping
                    </div>
                    <PayPal productId={product.id} />
                </div>
                <div>
                    <div>
                        ships from
                    </div>
                    <div>
                        Pinckney, MI
                    </div>
                    <div>
                        returns & exchanges
                    </div>
                    <div>
                        You have 14 days from item delivery to ship this item back. Buyer is responsible for return shipping costs. If the item is not returned in its original condition, the buyer is responsible for any loss in value.
                    </div>
                </div>
            </div>
        </div>
    {/await}
</div>

<style>
    .wrapper {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;
    }

    .row {
        display: flex;
        flex-direction: row;
    }

    .column {
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .column * {
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    img {
        width: 89%;
    }
</style>
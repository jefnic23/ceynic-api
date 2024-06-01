<script lang="ts">
	import type { PageData } from './$types';

	export let data: PageData;

    let sort: string = "";

    async function handleSort(event: Event) {
        sort = (event.target as HTMLSelectElement).value;
        const url = new URL(window.location.href);
        url.searchParams.set('sort', sort);
        window.location.href = url.toString();
    }
</script>

<div class="row">
	<div class="column small">
		<div>Filter</div>
	</div>
	<div class="column large">
		{#await data.products}
			<div>loading products...</div>
		{:then products}
			<div class="row">
				<div>
					Sort by:
					<select on:change={handleSort} bind:value={sort}>
                        <option value=""></option>
						<option value="price_asc">Price (low - high)</option>
						<option value="price_desc">Price (high - low)</option>
						<option value="size_asc">Size (small - large)</option>
						<option value="size_desc">Size (large - small)</option>
					</select>
				</div>
				<div>
					Results: {products.length}
				</div>
			</div>
			<div class="container">
				{#each products as product}
					<div class="item">
						{#if product.imageUrl}
							<a href="/products/{product.id}" data-sveltekit-preload-data>
								<img src={product.imageUrl} alt={product.title} />
							</a>
						{/if}
					</div>
				{/each}
			</div>
		{:catch error}
			<div>Something went wrong: {error.message}</div>
		{/await}
	</div>
</div>

<style>
	.row {
		display: flex;
		flex-direction: row;
		width: 100%;
		justify-content: space-between;
	}

	.column {
		display: flex;
		flex-direction: column;
	}

	.container {
		display: grid;
		grid-auto-columns: max-content;
		grid-auto-flow: dense;
		grid-auto-rows: minmax(100px, auto);
		grid-gap: 25px;
		grid-template-columns: repeat(3, 1fr);
	}

	.item {
		grid-row: span 1;
		grid-column: span 1;
	}

	.small {
		flex: 1;
	}

	.large {
		flex: 3;
	}

	img {
		max-width: 225px;
		object-fit: contain;
	}
</style>

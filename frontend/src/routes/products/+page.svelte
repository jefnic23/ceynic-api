<script lang="ts">
	import type { PageData } from './$types';
	import { goto } from '$app/navigation';

	export let data: PageData;

	let sort: string = '';

	async function handleSort(event: Event) {
		sort = (event.target as HTMLSelectElement).value;
		goto(`products?sort=${sort}`, { replaceState: true, keepFocus: true });
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
						<option value="oldest">Oldest</option>
						<option value="newest">Newest</option>
						<option value="price_asc">Lowest Price</option>
						<option value="price_desc">Highest Price</option>
						<option value="size_asc">Smallest</option>
						<option value="size_desc">Largest</option>
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
		padding: 1rem;
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
		margin: auto;
	}

	.small {
		flex: 1;
		border-right: 1px solid #e7e7e7;
	}

	.large {
		flex: 3;
		row-gap: 1rem;
	}

	img {
		max-width: 225px;
		object-fit: contain;
	}
</style>

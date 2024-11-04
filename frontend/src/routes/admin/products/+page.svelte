<script lang="ts">
	import Modal from '$lib/components/Modal.svelte';
	import type { Product } from '$lib/interfaces/product';
	import type { PageData } from './$types';

	export let data: PageData;

	let showModal: boolean = false;
	let selectedProduct: Product;

	async function openEditModal(product: Product) {
		const response = await fetch(`http://127.0.0.1:8000/products/${product.id}`);

        if (response.status !== 200) {
            console.log("Error retrieving product.");
        }
    
        const responseData = await response.json();

		selectedProduct = { ...responseData };
		showModal = true;
	}

	const currencyFormatter = new Intl.NumberFormat('en-US', {
		style: 'currency',
		currency: 'USD',
		minimumFractionDigits: 2
	});

	let hoverImage: string | null = null;
	let hoverPosition = { x: 0, y: 0 };

	function showImage(product: Product, event: MouseEvent) {
		hoverImage = product.imageUrl;
		hoverPosition = { x: event.clientX + 20, y: event.clientY - 50 }; // Adjust positioning as needed
	}

	function hideImage() {
		hoverImage = null;
	}
</script>

<table>
	{#await data.products}
		<div>loading products...</div>
	{:then products}
		<thead>
			<tr>
				<th>Title</th>
				<th>Price</th>
				<th>Height</th>
				<th>Width</th>
				<th>Medium</th>
				<th></th>
			</tr>
		</thead>
		<tbody>
			{#each products as product}
				<tr on:mouseenter={(event) => showImage(product, event)} on:mouseleave={hideImage}>
					<td>{product.title}</td>
					<td>{currencyFormatter.format(product.price)}</td>
					<td>{product.height}</td>
					<td>{product.width}</td>
					<td>{product.medium}</td>
					<td><button on:click={async () => await openEditModal(product)}>Edit</button></td>
				</tr>
			{/each}
		</tbody>
	{:catch error}
		<div>Something went wrong: {error.message}</div>
	{/await}
</table>

{#if hoverImage}
	<img
		src={hoverImage}
		class="hover-image visible"
		alt={hoverImage}
		style="top: {hoverPosition.y}px; left: {hoverPosition.x}px"
	/>
{/if}

{#if showModal}
	<Modal bind:showModal>
		<div class="edit">
			<input type="text" value={selectedProduct.title} />
			<input type="number" min="0.01" step="0.01" value={selectedProduct.price} />
			<input type="number" min="1" step="1" value={selectedProduct.height} />
			<input type="number" min="1" step="1" value={selectedProduct.width} />
			<select name="medium" bind:value={selectedProduct.medium}>
				<option value="Painting">Painting</option>
				<option value="Print">Print</option>
			</select>
		</div>
	</Modal>
{/if}

<style>
	table {
		width: 89%;
		border-radius: 8px;
		border-collapse: collapse;
		text-align: left;
	}

	tr {
		height: 34px;
	}

	.hover-image {
		position: fixed;
		display: none;
		border: 1px solid #ccc;
		max-width: 200px;
		max-height: 200px;
		pointer-events: none;
	}

	.hover-image.visible {
		display: block;
	}

	.edit {
		display: flex;
		flex-direction: column;
	}
</style>

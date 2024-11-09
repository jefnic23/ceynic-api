<script lang="ts">
	import Dropzone from '$lib/components/Dropzone.svelte';
	import Modal from '$lib/components/Modal.svelte';
	import Info from '$lib/icons/Info.svelte';
	import type { ProductOut, ProductsOut } from '$lib/interfaces/product';
	import type { PageData } from './$types';

	export let data: PageData;

	let showModal: boolean = false;
	let loadingModal: boolean = false;
	let selectedProduct: ProductOut;

	async function openEditModal(product: ProductsOut) {
		showModal = true;
		loadingModal = true;
		const response = await fetch(`http://127.0.0.1:8000/products/${product.id}`);

		if (response.status !== 200) {
			console.log('Error retrieving product.');
			loadingModal = false;
			showModal = false;
			return;
		}

		const responseData = await response.json();

		selectedProduct = { ...responseData };
		selectedProduct.images = selectedProduct.images.map(replaceImageUrl);
		loadingModal = false;
	}

	function replaceImageUrl(imageUrl: string) {
		const filename = imageUrl.split('/').at(-1);
		return `/api/proxy/${selectedProduct.title.replaceAll(' ', '_')}/${filename}`;
	}

	const currencyFormatter = new Intl.NumberFormat('en-US', {
		style: 'currency',
		currency: 'USD',
		minimumFractionDigits: 2
	});

	let hoverImage: string | null = null;
	let hoverPosition = { x: 0, y: 0 };
	let tableElement: Element;

	function showImage(product: ProductsOut, event: MouseEvent) {
		hoverImage = product.imageUrl;
		const tableRect = tableElement.getBoundingClientRect();
		const isCursorOnLeft = event.clientX < tableRect.left + tableRect.width / 2;
		hoverPosition = {
			x: isCursorOnLeft ? event.clientX + 20 : event.clientX - 220, // Adjust for image width
			y: event.clientY - 50
		};
	}

	function hideImage() {
		hoverImage = null;
	}

	let images: File[] = [];

	function handleImagesChange(event: CustomEvent<{ files: File[] }>) {
		images = event.detail.files;
	}

	function handleThumbnailChange(event: CustomEvent<{ thumbnail: string }>) {
		selectedProduct.thumbnail = event.detail.thumbnail;
	}

	function handleSubmit(event: Event) {
		event.preventDefault();
		console.log(selectedProduct);
		// const formData = new FormData(event.target as HTMLFormElement);
		// images.forEach((image) => formData.append('images', image));
		// Send `formData` to your API endpoint
	}
</script>

<table bind:this={tableElement}>
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
					<td>
						<button on:click={async () => await openEditModal(product)}>Edit</button>
					</td>
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
		{#if loadingModal}
			<div>loading product...</div>
		{:else}
			<div class="edit">
				<div class="edit-header">
					<Info color="#1e90ff" width="2em" height="2em" />
					<div>Edit Product</div>
				</div>

				<div class="form-input">
					<label for="title">Title</label>
					<input id="title" type="text" value={selectedProduct.title} />
				</div>
				<div class="form-input">
					<label for="description">Description</label>
					<textarea id="description" value={selectedProduct.description} />
				</div>

				<div class="form-row">
					<div class="form-input">
						<label for="price">Price</label>
						<div class="price">
							<input
								id="price"
								type="number"
								min="0.01"
								step="0.01"
								value={selectedProduct.price}
							/>
						</div>
					</div>

					<div class="form-input">
						<label for="medium">Medium</label>
						<select id="medium" bind:value={selectedProduct.medium}>
							<option value="Painting">Painting</option>
							<option value="Print">Print</option>
						</select>
					</div>
				</div>

				<div class="form-row">
					<div class="form-input">
						<label for="height">Height</label>
						<div class="inches">
							<input id="height" type="number" min="1" step="1" value={selectedProduct.height} />
						</div>
					</div>

					<div class="form-input">
						<label for="width">Width</label>
						<div class="inches">
							<input id="width" type="number" min="1" step="1" value={selectedProduct.width} />
						</div>
					</div>
				</div>

				<Dropzone
					on:change={handleImagesChange}
					on:thumbnailChange={handleThumbnailChange}
					previews={selectedProduct.images}
					thumbnail={selectedProduct.thumbnail}
				/>

				<div class="form-input">
					<button type="submit" on:click={handleSubmit}>Submit</button>
				</div>

				<!-- <div class="image-container">
					{#each selectedProduct.images as image}
						<div class="image-wrapper">
							<img src={image} alt={image} />
							{#if image.endsWith(selectedProduct.thumbnail)}
								<div class="thumbnail-overlay">
									<Thumbnail width="3em" height="3em" />
								</div>
							{/if}
						</div>
					{/each}
				</div> -->
			</div>
		{/if}
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

	textarea {
		resize: vertical;
		height: 89px;
	}

	input {
		width: 100%;
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
		row-gap: 1rem;
	}

	.form-row {
		display: flex;
		flex-direction: row;
		align-items: center;
		justify-content: space-between;
		column-gap: 1rem;
	}

	.form-input {
		display: flex;
		flex-direction: column;
		flex: 1;
	}

	.price {
		position: relative;
		display: inline-block;
	}

	.price input {
		padding-left: 1.5em; /* Add space for the dollar sign */
	}

	.price::before {
		content: '$';
		position: absolute;
		left: 0.5em; /* Adjust positioning as needed */
		top: 50%;
		transform: translateY(-50%);
		font-size: 1em;
		font-weight: bold;
		color: #333; /* Adjust color as needed */
	}

	.inches {
		position: relative;
		display: inline-block;
	}

	.inches input {
		padding-right: 2em;
	}

	.inches::after {
		content: 'in.';
		position: absolute;
		right: 0.34em; /* Adjust positioning as needed */
		top: 50%;
		transform: translateY(-50%);
		line-height: normal;
		font-size: 1em;
		font-weight: bold;
		color: #333; /* Adjust color as needed */
	}

	.edit-header {
		display: flex;
		flex-direction: row;
		justify-content: center;
		align-items: center;
		line-height: normal;
	}
</style>

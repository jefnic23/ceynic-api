<script lang="ts">
	import type { PageData } from './$types';

	export let data: PageData;

	const currencyFormatter = new Intl.NumberFormat('en-US', {
		style: 'currency',
		currency: 'USD',
		minimumFractionDigits: 2
	});
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
			</tr>
		</thead>
		<tbody>
			{#each products as product}
				<tr>
					<td>{product.title}</td>
					<td>{currencyFormatter.format(product.price)}</td>
					<td>{product.height}</td>
					<td>{product.width}</td>
					<td>{product.medium}</td>
				</tr>
			{/each}
		</tbody>
	{:catch error}
		<div>Something went wrong: {error.message}</div>
	{/await}
</table>

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
</style>

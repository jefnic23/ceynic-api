<script lang="ts">
	import Login from '$lib/components/Login.svelte';
	import type { PageData } from './$types';

	export let data: PageData;

	let user = data.user;
	$: showModal = !user;

	function handleLoginSuccess(event: any) {
		user = event.detail.user;
	}
</script>

{#if showModal}
	<Login on:loginSuccess={handleLoginSuccess} />
{:else}
	<div>
		<h1>hello world</h1>
	</div>
{/if}

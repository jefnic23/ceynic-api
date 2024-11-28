<script lang="ts">
	import type { LayoutData } from './$types';
	import { fly } from 'svelte/transition';
	import { cubicIn, cubicOut } from 'svelte/easing';
	import Login from '$lib/components/Login.svelte';
	import Sidebar from '$lib/components/Sidebar.svelte';
	

	export let data: LayoutData;

	let user = data.user;
	$: showModal = !user;

	function handleLoginSuccess(event: any) {
		user = event.detail.user;
	}
</script>

{#if showModal}
	<Login on:loginSuccess={handleLoginSuccess} />
{:else}
	<div class="container">
		<Sidebar />
    
		{#key data.url}
			<main
				in:fly={{ y: -34, duration: 144, delay: 233, easing: cubicOut }}
				out:fly={{ y: 34, duration: 144, easing: cubicIn }}
			>
				<slot />
			</main>
		{/key}
	</div>
{/if}

<style>
	.container {
		display: flex;
		flex-direction: row;
	}

	main {
		width: 100%;
		display: flex;
		justify-content: center;
		align-items: flex-start;
		margin: 1rem;
	}
</style>
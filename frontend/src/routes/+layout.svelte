<script lang="ts">
	import { fly } from 'svelte/transition';
	import { cubicIn, cubicOut } from 'svelte/easing';
	import '../app.css';
	import image from '$lib/header.jpg';
	import type { PageData } from './$types';
	import Header from '$lib/components/Header.svelte';
	import Footer from '$lib/components/Footer.svelte';

	export let data: PageData;
</script>

<div class="wrapper">
	<Header>
		<nav>
			<a href="/" data-sveltekit-preload-data>Home</a>
			<a href="/products" data-sveltekit-preload-data>Browse</a>
			<a href="/about">About</a>
			<a href="/contact">Contact</a>
		</nav>
	</Header>
	
	<img class="hero" src={image} alt="header.jpg" />

	{#key data.url}
		<main
			in:fly={{ y: -34, duration: 144, delay: 233, easing: cubicOut }}
			out:fly={{ y: 34, duration: 144, easing: cubicIn }}
		>
			<slot />
		</main>
	{/key}

	<Footer />
</div>

<style>
	nav {
		min-height: 50px;
		background-color: #f8f8f8;
		border: 1px solid #e7e7e7;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	nav a {
		text-transform: uppercase;
		margin: 0 0.5rem;
		color: rgba(0, 0, 0, 0.55);
		font-size: 13px;
		transition:
			color 0.15s ease-in-out,
			background-color 0.15s ease-in-out,
			border-color 0.15s ease-in-out;
	}

	a {
		text-decoration: none;
	}

	main {
		display: flex;
		justify-content: center;
		flex: 1;
		padding: 1rem;
	}

	.hero {
		max-width: 100%;
		border-bottom: 1px solid #e7e7e7;
		position: relative;
		margin-top: 50px;

	}

	.wrapper {
		min-height: 100svh;
		display: flex;
		flex-direction: column;
		justify-content: space-between;
	}
</style>

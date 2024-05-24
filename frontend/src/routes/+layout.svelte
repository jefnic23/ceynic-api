<script lang="ts">
    import "../app.css"
	import Etsy from '$lib/icons/etsy.svelte';
	import Instagram from '$lib/icons/instagram.svelte';
	import Pinterest from '$lib/icons/pinterest.svelte';
	import image from '$lib/header.jpg';

	let year: number = new Date().getFullYear();
</script>

<div class="wrapper">
	<div>
		<nav>
			<a href="/">Home</a>
			<a href="/browse">Browse</a>
			<a href="/about">About</a>
			<a href="/contact">Contact</a>
		</nav>

		<img src={image} alt="header.jpg" />
	</div>

	<main>
		<slot></slot>
	</main>

	<div class="footer">
		<div class="icons">
			<a href="https://www.etsy.com/shop/TraceyNicholasArt" target="_blank" class="icon etsy">
				<Etsy />
			</a>
			<a
				href="https://www.instagram.com/traceynicholas_art/"
				target="_blank"
				class="icon instagram"
			>
				<Instagram />
			</a>
			<a href="https://www.pinterest.com/tnicholas48169/" target="_blank" class="icon pinterest">
				<Pinterest />
			</a>
		</div>
		<div class="copyright">
			Copyright © {year}, Tracey Nicholas. All rights reserved. |
			<a href="/login" style="color: #666666;">Administration</a> | Site by
			<a href="https://github.com/jefnic23" target="_blank">Jeff Nicholas</a>
		</div>
	</div>
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

	img {
		max-width: 100%;
		border-bottom: 1px solid #e7e7e7;
		position: relative;
	}

    main {
        display: flex;
		justify-content: center;
		flex: 1;
    }

	.wrapper {
		min-height: 100svh;
		display: flex;
		flex-direction: column;
		justify-content: space-between;
	}

	.footer {
		display: flex;
		flex-direction: column;
		align-items: center;
        gap: 1rem;
        padding: 1rem;
	}

	.icons {
		display: flex;
		flex-direction: row;
		align-items: center;
        gap: 1rem;
	}

	.icon {
		display: flex;
		flex-direction: row;
		justify-content: center;
		align-items: center;
        height: 32px;
		width: 32px;
	}

	.etsy {
		border: #fd7e14 solid 1px;
		border-radius: 50%;
		background-color: #fd7e14;
		padding: 3px;
		color: white;
	}

	.instagram {
		background-clip: text;
		-webkit-text-fill-color: transparent;
	}

	.pinterest {
		color: red;
	}

    .copyright {
        font-size: 10px;
    }
</style>

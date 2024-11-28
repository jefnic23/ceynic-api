<script lang="ts">
	import { enhance } from "$app/forms";
	import Hamburger from "$lib/icons/Hamburger.svelte";
    import Home from '$lib/icons/Home.svelte';
	import Listing from '$lib/icons/Listing.svelte';
	import Logout from "$lib/icons/Logout.svelte";
	import Button from "./Button.svelte";

    let open: boolean = false
</script>

<aside class:open>
    <Hamburger />
    <nav>
        <a href="/admin"><Home /> Home</a>
        <a href="/admin/products"><Listing /> Products</a>
		<form action="/admin/logout" method="POST" use:enhance>
			<button><Logout /> Log Out</button>
		</form>
    </nav>
</aside>

<style>
    aside {
		width: 144px;
        height: 100vh;
        background-color: #f8f8f8;
		border: 1px solid #e7e7e7;
		display: flex;
		flex-direction: column;
		align-items: flex-start;
		justify-content: flex-start;
	}

    nav {
        display: flex;
        flex-direction: column;
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

    .open {
        width: 200px;
    }
</style>
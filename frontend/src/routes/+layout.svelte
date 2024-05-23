<script lang="ts">
    import Etsy from "$lib/icons/etsy.svelte";
    import Instagram from "$lib/icons/instagram.svelte";
    import Pinterest from "$lib/icons/pinterest.svelte";

    let year: number = new Date().getFullYear();
</script>

<nav>
    <a href="/">Home</a>
    <a href="/browse">Browse art</a>
    <a href="/about">About</a>
    <a href="/contact">Contact</a>
</nav>

<slot></slot>

<div class="footer">
    <div class="social-icons">
        <a href="https://www.etsy.com/shop/TraceyNicholasArt" target="_blank">
            <Etsy />
        </a>
        <a href="https://www.instagram.com/traceynicholas_art/" target="_blank">
            <Instagram />
        </a>
        <a href="https://www.pinterest.com/tnicholas48169/" target="_blank">
            <Pinterest />
        </a>
    </div>
    <div class="copyright">
        Copyright © {year}, Tracey Nicholas. All rights reserved. | 
        <a href="/login" style="color: #666666;">Administration</a> | 
        Site by <a href="https://github.com/jefnic23" target="_blank">Jeff Nicholas</a>
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
        text-decoration: none;
        margin: 0 0.5rem;
        color: rgba(0, 0, 0, .55);
        font-size: 13px;
        font-family: 'Roboto', 'Helvetica Neue', Helvetica, Arial, sans-serif;
        transition: color .15s ease-in-out, background-color .15s ease-in-out, border-color .15s ease-in-out;
    }
</style>
<script lang="ts">
    import Etsy from '$lib/icons/etsy.svelte';
	import Instagram from '$lib/icons/instagram.svelte';
	import Pinterest from '$lib/icons/pinterest.svelte';

    let year: number = new Date().getFullYear();
</script>

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

<style>
    .footer {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 1rem;
		padding: 1rem;
		background-color: #f8f8f8;
		border: 1px solid #e7e7e7;
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
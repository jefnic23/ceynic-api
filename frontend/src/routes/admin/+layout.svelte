<script lang="ts">
    import { fly } from 'svelte/transition';
	import { cubicIn, cubicOut } from 'svelte/easing';
    import type { PageData } from './$types';

    export let data: PageData;
</script>

{#key data.url}
    <main
        in:fly={{ y: -34, duration: 144, delay: 233, easing: cubicOut }}
        out:fly={{ y: 34, duration: 144, easing: cubicIn }}
    >
        <slot />
    </main>
{/key}
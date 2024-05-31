<script lang="ts">
	import { createEventDispatcher } from 'svelte';

	export let duration = '233ms';
	export let offset = 0;
	export let tolerance = 0;

	let headerClass = 'pin';
	let lastHeaderClass = 'pin';
	let y = 0;
	let lastY = 0;

	const dispatch = createEventDispatcher();

	function deriveClass(y: number = 0, scrolled: number = 0): string {
		if (y < offset) return 'pin';
		if (!scrolled || Math.abs(scrolled) < tolerance) return headerClass;
		return scrolled < 0 ? 'unpin' : 'pin';
	}

	function updateClass(y: number = 0): string {
		const scrolledPxs = lastY - y;
		const result = deriveClass(y, scrolledPxs);
		lastY = y;
		return result;
	}

	function action(node: HTMLElement): void {
		node.style.transitionDuration = duration;
	}

	$: {
		headerClass = updateClass(y);
		if (headerClass !== lastHeaderClass) {
			dispatch(headerClass);
		}
		lastHeaderClass = headerClass;
	}
</script>

<svelte:window bind:scrollY={y} />

<div use:action class={headerClass}>
	<slot />
</div>

<style>
	div {
		position: fixed;
		width: 100%;
		top: 0;
		transition: transform 233ms linear;
		z-index: 999;
	}

	.pin {
		transform: translateY(0%);
	}

	.unpin {
		transform: translateY(-100%);
	}
</style>

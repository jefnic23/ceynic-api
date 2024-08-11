<script lang="ts">
	export let showModal: boolean;
	export let showClose: boolean = true;
	export let type: 'info' | 'success' | 'warning' | 'error' = 'info';

	let dialog: HTMLDialogElement;

	$: if (dialog && showModal) dialog.showModal();
</script>

<!-- svelte-ignore a11y-click-events-have-key-events a11y-no-noninteractive-element-interactions -->
<dialog
	bind:this={dialog}
	on:close={() => (showModal = false)}
	class={type}
>
	<!-- svelte-ignore a11y-no-static-element-interactions -->
	<div on:click|stopPropagation>
		<slot />
		<!-- svelte-ignore a11y-autofocus -->
		{#if showClose}
			<button autofocus on:click={() => dialog.close()}>close</button>
		{/if}
	</div>
</dialog>

<style>
	dialog {
		max-width: 32em;
		border-radius: 0.5em;
		border: none;
		padding: 0;
	}

	dialog::backdrop {
		background: rgba(0, 0, 0, 0.3);
	}

	dialog > div {
		padding: 1em;
	}

	dialog[open] {
		animation: zoom 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
	}

	@keyframes zoom {
		from {
			transform: scale(0.95);
		}
		to {
			transform: scale(1);
		}
	}

	dialog[open]::backdrop {
		animation: fade 0.2s ease-out;
	}

	@keyframes fade {
		from {
			opacity: 0;
		}
		to {
			opacity: 1;
		}
	}
    
	button {
		display: block;
	}

	/* Colored bar on the left edge */
	dialog::before {
		content: '';
		position: absolute;
		left: 0;
		top: 0;
		bottom: 0;
		width: 0.5em;
		border-radius: 0.5em 0 0 0.5em;
		background-color: var(--modal-bar-color);
	}

	/* Modal types */
	.info::before {
		--modal-bar-color: #1e90ff; /* Blue for info */
	}

	.success::before {
		--modal-bar-color: #28a745; /* Green for success */
	}

	.warning::before {
		--modal-bar-color: #ffcc00; /* Yellow for warning */
	}

	.error::before {
		--modal-bar-color: #ff6347; /* Red for error */
	}
</style>

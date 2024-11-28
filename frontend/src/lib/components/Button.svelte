<script lang="ts">
	import { createEventDispatcher } from 'svelte';

	export let text: string;
	export let style: 'submit' | 'cancel' | 'info' | 'warning' = 'submit';
	export let icon: string | null = null;
	export let iconPosition: 'left' | 'right' = 'left';
	export let size: 'small' | 'medium' | 'large' = 'medium';
	export let disabled: boolean = false;
	export let loading: boolean = false;
	export let fullWidth: boolean = false;
	export let tooltip: string | null = null;

	const dispatch = createEventDispatcher();

	function handleClick(event: Event) {
		if (!disabled && !loading) {
			dispatch('click', event);
		}
	}
</script>

<button
	class="{style} {size} {fullWidth ? 'full-width' : ''} {disabled ? 'disabled' : ''}"
	on:click={handleClick}
	{disabled}
	title={tooltip}
>
	{#if loading}
		<span class="spinner"></span>
	{:else}
		{#if icon && iconPosition === 'left'}
			<img src={icon} alt="" class="icon-left" />
		{/if}
		<span>{text}</span>
		{#if icon && iconPosition === 'right'}
			<img src={icon} alt="" class="icon-right" />
		{/if}
	{/if}
</button>

<style>
	button {
		display: inline-flex;
		align-items: center;
		justify-content: center;
		border: none;
		cursor: pointer;
		padding: 0.5rem 1rem;
		font-size: 1rem;
		border-radius: 0.25rem;
		transition:
			background-color 0.3s ease,
			transform 0.2s ease,
			box-shadow 0.2s ease;
	}

	/* Style Variants */
	.submit {
		background-color: #4caf50;
		color: white;
	}
	.cancel {
		background-color: #f44336;
		color: white;
	}
	.info {
		background-color: #2196f3;
		color: white;
	}
	.warning {
		background-color: #ff9800;
		color: white;
	}

	/* Size Variants */
	.small {
		font-size: 0.75rem;
		padding: 0.25rem 0.5rem;
	}
	.medium {
		font-size: 1rem;
		padding: 0.5rem 1rem;
	}
	.large {
		font-size: 1.25rem;
		padding: 0.75rem 1.5rem;
	}

	/* Full Width */
	.full-width {
		width: 100%;
	}

	/* Disabled State */
	button:disabled,
	.disabled {
		background-color: #e0e0e0;
		color: #9e9e9e;
		cursor: not-allowed;
	}

	/* Loading Spinner */
	.spinner {
		border: 2px solid rgba(255, 255, 255, 0.6);
		border-top: 2px solid white;
		border-radius: 50%;
		width: 1em;
		height: 1em;
		animation: spin 0.6s linear infinite;
	}

	@keyframes spin {
		0% {
			transform: rotate(0deg);
		}
		100% {
			transform: rotate(360deg);
		}
	}

	/* Hover Effects */
	button:hover {
		transform: scale(1.03); /* Slight scale-up effect */
		box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Adds a subtle shadow */
	}
</style>

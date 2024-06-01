<script lang="ts">
	import { PUBLIC_RECAPTCHA_SITE_KEY } from '$env/static/public';
	import type { ActionResult } from '@sveltejs/kit';
	import type { ActionData } from './$types';
	import { applyAction, deserialize } from '$app/forms';
	import { invalidateAll } from '$app/navigation';

	export let form: ActionData;

	async function handleSubmit(event: SubmitEvent) {
		window.grecaptcha.ready(async () => {
			const token = await window.grecaptcha.execute(PUBLIC_RECAPTCHA_SITE_KEY, {
				action: 'submit'
			});

			const data = new FormData(event.target as HTMLFormElement);

			data.append('token', token);

			const response = await fetch((event.target as HTMLFormElement).action, {
				method: (event.target as HTMLFormElement).method,
				body: data
			});

			const result: ActionResult = deserialize(await response.text());

			if (result.type === 'success') {
				await invalidateAll();
			}

			applyAction(result);
		});
	}
</script>

<svelte:head>
	<script src="https://www.google.com/recaptcha/api.js?render={PUBLIC_RECAPTCHA_SITE_KEY}"></script>
</svelte:head>

<div class="wrapper">
	<h3>Please contact me if you have any questions or comments</h3>
	<form class="wrapper form" method="POST" on:submit|preventDefault={handleSubmit}>
		{#if form?.success}
			<div>Thank you for your message!</div>
		{:else}
			<div class="form-element">
				<label class="form-label" for="name">Name</label>
				<input
					class="form-control"
					id="name"
					name="name"
					type="text"
					value=""
					placeholder="Your name..."
					required
				/>
			</div>
			<div class="form-element">
				<label class="form-label" for="email">Email</label>
				<input
					class="form-control"
					id="email"
					name="email"
					type="text"
					value=""
					placeholder="Your email..."
					required
				/>
			</div>
			<div class="form-element">
				<label class="form-label" for="message">Message</label>
				<textarea
					class="form-control"
					id="message"
					name="message"
					placeholder="Write something..."
					required
				></textarea>
			</div>
			<div class="recaptcha">
				This site is protected by reCAPTCHA and the Google
				<a href="https://policies.google.com/privacy" target="_blank">Privacy Policy</a> and
				<a href="https://policies.google.com/terms" target="_blank">Terms of Service</a> apply.
			</div>
			<button>Send</button>
		{/if}
	</form>
</div>

<style>
	.wrapper {
		display: flex;
		flex-direction: column;
		align-items: center;
		width: 100%;
		gap: 1rem;
	}

	.form {
		max-width: 500px;
	}

	.form-element {
		display: flex;
		flex-direction: column;
		align-items: flex-start;
		width: 100%;
	}

	.form-control {
		width: 100%;
		border: 2px solid #666;
		border-radius: 0.34rem;
	}

	.recaptcha {
		font-size: 11px;
	}

	button,
	input,
	textarea {
		font-family: inherit;
		font-size: 100%;
		padding: 0.5rem;
	}

	textarea {
		resize: none;
	}

	:global(.grecaptcha-badge) {
		visibility: hidden;
	}
</style>

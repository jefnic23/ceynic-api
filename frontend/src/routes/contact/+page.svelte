<script lang="ts">
	import { PUBLIC_RECAPTCHA_SITE_KEY } from '$env/static/public';
	import type { ActionResult } from '@sveltejs/kit';
	import type { ActionData } from './$types';
	import { applyAction, deserialize } from '$app/forms';
	import { invalidateAll } from '$app/navigation';

	export let form: ActionData;

	async function handleSubmit(event: SubmitEvent) {
		window.grecaptcha.ready(async () => {
			const token = await window.grecaptcha.execute(PUBLIC_RECAPTCHA_SITE_KEY, { action: 'submit' });

			console.log(event);

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
	<form method="POST" on:submit|preventDefault={handleSubmit}>
		{#if form?.success}
			<div>Thank you for reaching out!</div>
		{:else}
			<div>
				<label class="form-label" for="name">Name</label>
				<input class="form-control" id="name" name="name" type="text" value="" required />
			</div>
			<div>
				<label class="form-label" for="email">Email</label>
				<input class="form-control" id="email" name="email" type="text" value="" required />
			</div>
			<div>
				<label class="form-label" for="message">Message</label>
				<textarea class="form-control" id="message" name="message" required></textarea>
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
	}
</style>

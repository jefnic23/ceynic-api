<script lang="ts">
	import Modal from '$lib/components/Modal.svelte';
	import Person from '$lib/icons/Person.svelte';
	import Lock from '$lib/icons/Lock.svelte';
	import { createEventDispatcher } from 'svelte';
	import Button from './Button.svelte';
	
	export let invalid: boolean = false;
	export let credentials: boolean = false;

	const dispatch = createEventDispatcher();

	async function handleSubmit(event: Event): Promise<void> {
		const formEl = event.target as HTMLFormElement;
		const data = new FormData(formEl);

		const response = await fetch(formEl.action, {
			method: formEl.method,
			body: data
		});

		let responseData = await response.json();

		if (response.status == 200 && responseData.success == true) {
            dispatch('loginSuccess', { user: "me" });
        } else if (response.status == 401) {
            console.log("Username or password incorrect.");
        } else {
            console.log("Error logging in.");
        }
	}
</script>

<Modal showModal={true} showClose={false} title="Log In">
	<div class="body">
		<form action="/admin/login" method="POST" on:submit|preventDefault={handleSubmit}>
			<div class="input-container">
				<Person />
				<input id="email" name="username" value="" placeholder="Email" type="email" required />
			</div>
			<div class="input-container">
				<Lock />
				<input
					id="password"
					name="password"
					value=""
					placeholder="Password"
					type="password"
					required
				/>
			</div>
			{#if invalid}
				<p class="error">Username and password is required.</p>
			{/if}

			{#if credentials}
				<p class="error">You have entered the wrong credentials.</p>
			{/if}
			<Button text="Submit" />
		</form>
	</div>
</Modal>

<style>
	.body {
		display: flex;
		flex-direction: column;
		align-items: center;
		width: 377px;
	}

	form {
		display: flex;
		flex-direction: column;
		align-items: center;
		width: 100%;
	}

	.input-container {
		display: flex;
		align-items: center;
		margin-bottom: 1rem;
		border-bottom: 2px solid #ccc;
		width: 89%;
	}

	input {
		flex-grow: 1;
		padding: 0.5rem 0;
		border: none;
		outline: none;
		background-color: transparent;
		margin-left: 0.5em;
	}

	input::placeholder {
		color: #aaa;
	}

	input:-webkit-autofill,
	input:-webkit-autofill:hover,
	input:-webkit-autofill:focus {
		-webkit-box-shadow: 0 0 0px 1000px white inset !important;
		box-shadow: 0 0 0px 1000px white inset !important;
		-webkit-text-fill-color: #000 !important;
	}

	.input-container:focus-within {
		border-bottom-color: #007bff; /* Change this to your desired color */
	}

	button {
		margin-top: 1rem;
		padding: 0.75rem;
		background-color: #007bff;
		color: white;
		border: none;
		border-radius: 4px;
		cursor: pointer;
		width: 34%;
	}

	button:hover {
		background-color: #0056b3;
	}
</style>

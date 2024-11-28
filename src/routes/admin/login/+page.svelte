<script lang="ts">
	import type { ActionData } from './$types';
	import Person from '$lib/icons/Person.svelte';
	import Lock from '$lib/icons/Lock.svelte';

	export let form: ActionData;
</script>

<div class="body">
	<h2>Log In</h2>
	<form action="?/login" method="POST">
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
		{#if form?.credentials}
			<p class="error">You have entered the wrong credentials.</p>
		{/if}
		<button>Submit</button>
	</form>
</div>

<style>
	.body {
		display: flex;
		flex-direction: column;
		align-items: center;
		width: 377px;
	}

	h2 {
		text-transform: uppercase;
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

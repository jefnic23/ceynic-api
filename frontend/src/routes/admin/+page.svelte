<script lang="ts">
	import Modal from '$lib/components/Modal.svelte';
    import { accessToken, refreshToken } from "$lib/stores/tokens";
    import { user, getUser } from "$lib/stores/users";
    import { type Token } from "$lib/interfaces/token";

	let showModal: boolean = true;

	async function handleSubmit(event: Event): Promise<void> {
		const formEl = event.target as HTMLFormElement;
		const data = new FormData(formEl);

		const response = await fetch(formEl.action, {
			method: formEl.method,
			body: data
		});

		if (response.status == 200) {
			const responseData: Token = await response.json();
			accessToken.set(responseData.accessToken);
			refreshToken.set(responseData.refreshToken);
			user.set(await getUser(responseData.accessToken));
		} else if (response.status == 401) {
			console.log('Username or password incorrect.');
		} else {
			console.log('Error logging in.');
		}
	}
</script>

<Modal bind:showModal showClose={false}>
	<h2 slot="header">Login</h2>
	<form method="post" action="http://127.0.0.1:8000/login" on:submit|preventDefault={handleSubmit}>
		<label for="email">Email</label>
		<input id="email" name="email" value="" placeholder="Your email..." required />
		<label for="password">Email</label>
		<input id="password" name="password" value="" placeholder="Your password..." required />
		<button>Submit</button>
	</form>
</Modal>

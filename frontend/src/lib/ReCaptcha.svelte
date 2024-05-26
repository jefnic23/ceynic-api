<script lang="ts">
	import { PUBLIC_RECAPTCHA_SITE_KEY } from '$env/static/public';
</script>

<svelte:head>
	<script src="https://www.google.com/recaptcha/api.js"></script>

	<script>
		function onSubmit(token) {
			console.log(token);
			// document.getElementById('contact-form').submit();
		}
	</script>
</svelte:head>

<button
    class="g-recaptcha"
    data-sitekey="{PUBLIC_RECAPTCHA_SITE_KEY}"
    data-callback="onSubmit"
    data-action="submit"
>
    Send
</button>

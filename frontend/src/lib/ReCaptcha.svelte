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
    data-sitekey="6LfZN-gpAAAAAG-Apw86KAsXLC4Yp52XefxzJi1i"
    data-callback="onSubmit"
    data-action="submit"
>
    Send
</button>

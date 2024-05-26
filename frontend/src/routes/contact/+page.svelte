<script lang="ts">
	import ReCaptcha from "$lib/ReCaptcha.svelte";
</script>

<div class="container-fluid form-group app-content">
	<h3>Please contact me if you have any questions or comments</h3>

	<form id="contact-form" action="" method="post" class="form">
		<div class="mb-3 required">
			<label class="form-label" for="name">Name</label>
			<input class="form-control" id="name" name="name" type="text" value="" required />
		</div>

		<div class="mb-3 required">
			<label class="form-label" for="email">Email</label>
			<input class="form-control" id="email" name="email" type="text" value="" required />
		</div>

		<div class="mb-3 required">
			<label class="form-label" for="msg">Message</label>
			<textarea class="form-control" id="msg" name="msg" required></textarea>
		</div>

		<ReCaptcha />
	</form>
</div>

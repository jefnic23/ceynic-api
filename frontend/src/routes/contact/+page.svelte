<div class="container-fluid form-group app-content">
	<h3>Please contact me if you have any questions or comments</h3>

	<form action="" method="post" class="form">
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

		<div class="mb-3">
			<label class="form-label" for="recaptcha"></label>

			<script src="https://www.google.com/recaptcha/api.js" async defer></script>
			<div class="g-recaptcha" data-sitekey="6LexjUYhAAAAAAT0UDg5Fb67837gamIULnYRFUia">
				<div style="width: 304px; height: 78px;">
					<div>
						<iframe
							title="reCAPTCHA"
							width="304"
							height="78"
							role="presentation"
							name="a-xaw59tud8oiv"
							frameborder="0"
							scrolling="no"
							sandbox="allow-forms allow-popups allow-same-origin allow-scripts allow-top-navigation allow-modals allow-popups-to-escape-sandbox allow-storage-access-by-user-activation"
							src="https://www.google.com/recaptcha/api2/anchor?ar=1&amp;k=6LexjUYhAAAAAAT0UDg5Fb67837gamIULnYRFUia&amp;co=aHR0cHM6Ly93d3cudHJhY2V5bmljaG9sYXMuY29tOjQ0Mw..&amp;hl=en&amp;v=joHA60MeME-PNviL59xVH9zs&amp;size=normal&amp;cb=s9bbk922nuo6"
						></iframe>
					</div>
					<textarea
						id="g-recaptcha-response"
						name="g-recaptcha-response"
						class="g-recaptcha-response"
						style="width: 250px; height: 40px; border: 1px solid rgb(193, 193, 193); margin: 10px 25px; padding: 0px; resize: none; display: none;"
					></textarea>
				</div>
			</div>
		</div>

		<input class="btn btn-primary btn-md" id="send" name="send" type="submit" value="Send" />
	</form>
</div>

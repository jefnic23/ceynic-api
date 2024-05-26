<script lang="ts">
	import { loadScript } from '@paypal/paypal-js';
	import { onMount } from 'svelte';
	import { PUBLIC_PAYPAL_CLIENT_ID } from '$env/static/public';

	export let amount: string;

	onMount(async () => {
		const paypal = await loadScript({
			clientId: PUBLIC_PAYPAL_CLIENT_ID,
			currency: 'USD',
			disableFunding: 'venmo',
			dataPageType: 'checkout'
		});

		if (
			paypal === undefined ||
			paypal === null ||
			paypal.Buttons === undefined ||
			paypal.Buttons === null
		) {
			return;
		}

		paypal
			.Buttons({
				createOrder: function (data, actions) {
					return actions.order.create({
						intent: 'CAPTURE',
						purchase_units: [
							{
								amount: {
									currency_code: 'USD',
									value: amount
								}
							}
						]
					});
				}
			})
			.render('#paypal-container-element');
	});
</script>

<div id="paypal-container-element"></div>

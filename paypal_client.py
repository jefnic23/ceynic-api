from paypalpayoutssdk.core import PayPalHttpClient, SandboxEnvironment
from app import app

class PayPalClient:
    def __init__(self):
        self.client_id = app.config['PAYPAL_CLIENT_ID']
        self.client_secret = app.config['PAYPAL_CLIENT_SECRET']
        """Set up and return PayPal Python SDK environment with PayPal Access credentials.
           This sample uses SandboxEnvironment. In production, use
           LiveEnvironment."""
        self.environment = SandboxEnvironment(client_id=self.client_id, client_secret=self.client_secret)
        """ Returns PayPal HTTP client instance in an environment with access credentials. Use this instance to invoke PayPal APIs, provided the
            credentials have access. """
        self.client = PayPalHttpClient(self.environment)

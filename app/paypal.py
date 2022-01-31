from paypalcheckoutsdk.core import PayPalHttpClient, LiveEnvironment
from paypalcheckoutsdk.orders import OrdersCreateRequest, OrdersCaptureRequest
from app import app

class PayPalClient:
    def __init__(self):
        self.client_id = app.config['PAYPAL_CLIENT_ID']
        self.client_secret = app.config['PAYPAL_CLIENT_SECRET']
        """Set up and return PayPal Python SDK environment with PayPal Access credentials.
           This sample uses SandboxEnvironment. In production, use
           LiveEnvironment."""
        self.environment = LiveEnvironment(client_id=self.client_id, client_secret=self.client_secret)
        """ Returns PayPal HTTP client instance in an environment with access credentials. Use this instance to invoke PayPal APIs, provided the
            credentials have access. """
        self.client = PayPalHttpClient(self.environment)

class CreateOrder(PayPalClient):
    @staticmethod
    def build_request_body(description, value):
        return \
            {
                "intent": "CAPTURE",
                "purchase_units": [
                    {
                        "description": description,
                        "amount": {
                            "currency_code": "USD",
                            "value": value
                        }
                    }
                ]
            }

    def create_order(self, description, value):
        request = OrdersCreateRequest()
        request.headers['prefer'] = 'return=representation'
        request.request_body(self.build_request_body(description, value))
        response = self.client.execute(request)
        # print(response.result.__dict__)
        return response

class CaptureOrder(PayPalClient):
    def capture_order(self, order_id):
        request = OrdersCaptureRequest(order_id)
        response = self.client.execute(request)
        # print(response.result.__dict__)
        return response

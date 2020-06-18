import json

import requests
from django.conf import settings
from requests.auth import HTTPBasicAuth

MPESA_SETTING = settings.PAYMENT.get('MPESA', {})
CONSUMER_KEY = MPESA_SETTING.get('CONSUMER_KEY')
CONSUMER_SECRET = MPESA_SETTING.get('CONSUMER_SECRET')


class Mpesa:

    def __init__(self, consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret

    @property
    def access_token(self):
        request = requests.get(
            r"https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials",
            auth=HTTPBasicAuth(self.consumer_key, self.consumer_secret),
        )
        return json.loads(request.text)['access_token']

    def b2c(self):
        return self._send_typed_transaction_request('b2c', {
            "InitiatorName": " ",
            "SecurityCredential": " ",
            "CommandID": " ",
            "Amount": " ",
            "PartyA": " ",
            "PartyB": " ",
            "Remarks": " ",
            "QueueTimeOutURL": "http://your_timeout_url",
            "ResultURL": "http://your_result_url",
            "Occasion": " ",
        }, )

    def b2b(self):
        return self._send_typed_transaction_request('b2b', {
            "Initiator": " ",
            "SecurityCredential": " ",
            "CommandID": " ",
            "SenderIdentifierType": " ",
            "RecieverIdentifierType": " ",
            "Amount": " ",
            "PartyA": " ",
            "PartyB": " ",
            "AccountReference": " ",
            "Remarks": " ",
            "QueueTimeOutURL": "http://your_timeout_url",
            "ResultURL": "http://your_result_url",
        })

    def c2b(self):
        return self._send_transaction_request(
            url=r'http://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl',
            request_data={
                "ShortCode": " ",
                "ResponseType": " ",
                "ConfirmationURL": "http://ip_address:port/confirmation",
                "ValidationURL": "http://ip_address:port/validation_url",
            },
        )

    def c2b_simulate(self):
        return self._send_transaction_request(
            url=r'https://sandbox.safaricom.co.ke/mpesa/c2b/v1/simulate',
            request_data={
                "ShortCode": " ",
                "CommandID": "CustomerPayBillOnline",
                "Amount": " ",
                "Msisdn": " ",
                "BillRefNumber": " ",
            },
        )

    def account_balance(self):
        return self._send_transaction_request(
            url=r'https://sandbox.safaricom.co.ke/mpesa/accountbalance/v1/query',
            request_data={
                "Initiator": " ",
                "SecurityCredential": " ",
                "CommandID": "AccountBalance",
                "PartyA": "shortcode",
                "IdentifierType": "4",
                "Remarks": "Remarks",
                "QueueTimeOutURL": "https://ip_address:port/timeout_url",
                "ResultURL": "https://ip_address:port/result_url",
            },
        )

    def transaction_status(self):
        """
        Transaction Status API checks the status of a B2B, B2C and C2B APIs transactions
        """
        return self._send_transaction_request(
            url=r'https://sandbox.safaricom.co.ke/mpesa/transactionstatus/v1/query',
            request_data={
                "Initiator": " ",
                "SecurityCredential": " ",
                "CommandID": "TransactionStatusQuery",
                "TransactionID": " ",
                "PartyA": " ",
                "IdentifierType": "1",
                "ResultURL": "https://ip_address:port/result_url",
                "QueueTimeOutURL": "https://ip_address:port/timeout_url",
                "Remarks": " ",
                "Occasion": " ",
            },
        )

    def reverse(self):
        """
        Reverses a B2B, B2C or C2B M-Pesa transaction
        """
        return self._send_transaction_request(
            url=r'https://sandbox.safaricom.co.ke/mpesa/reversal/v1/request',
            request_data={
                "Initiator": " ",
                "SecurityCredential": " ",
                "CommandID": "TransactionReversal",
                "TransactionID": " ",
                "Amount": " ",
                "ReceiverParty": " ",
                "RecieverIdentifierType": "4",
                "ResultURL": "https://ip_address:port/result_url",
                "QueueTimeOutURL": "https://ip_address:port/timeout_url",
                "Remarks": " ",
                "Occasion": " ",
            },
        )

    def lipa_na_mpesa(self):
        """
        Lipa na M-Pesa Online Payment API is used to initiate a M-Pesa transaction
        on behalf of a customer using STK Push. This is the same technique mySafaricom
         App uses whenever the app is used to make payments
        """
        return self._send_transaction_request(
            url=r'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest',
            request_data={
                "BusinessShortCode": " ",
                "Password": " ",
                "Timestamp": " ",
                "TransactionType": "CustomerPayBillOnline",
                "Amount": " ",
                "PartyA": " ",
                "PartyB": " ",
                "PhoneNumber": " ",
                "CallBackURL": "https://ip_address:port/callback",
                "AccountReference": " ",
                "TransactionDesc": " ",
            },
        )

    def lipa_na_mpesa_query(self):
        return self._send_transaction_request(
            url=r'https://sandbox.safaricom.co.ke/mpesa/stkpushquery/v1/query',
            request_data={
                "BusinessShortCode": " ",
                "Password": " ",
                "Timestamp": " ",
                "CheckoutRequestID": " ",
            },
        )

    def _send_typed_transaction_request(self, type: str, request_data: dict):
        return self._send_transaction_request(
            f'https://sandbox.safaricom.co.ke/mpesa/{type}/v1/paymentrequest',
            request_data,
        )

    def _send_transaction_request(self, url: str, request_data: dict, ):
        request = requests.post(
            url=url,
            json=request_data,
            headers={
                'Authorization': f'Bearer {self.access_token}'
            },
        )
        return json.loads(request.text)

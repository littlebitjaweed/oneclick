from twilio.rest import Client
import random
from .models import OTP
import os

TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
VERIFY_SERVICE_SID  = os.environ.get('VERIFY_SERVICE_SID')


client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


def format_phone_number(phone):
    if not phone.startswith('+'):
        return '+91' + phone  # Default to India country code
    return phone


def send_otp(phone_number):
    formatted_phone = format_phone_number(phone_number)

    verification = client.verify.v2.services(VERIFY_SERVICE_SID).verifications.create(
        to= formatted_phone,
        channel='sms'  # Can also use 'call' or 'email' if enabled
    )
    return verification.status

def check_otp(phone_number, code):
    formatted_phone = format_phone_number(phone_number)
    verification_check = client.verify.v2.services(VERIFY_SERVICE_SID).verification_checks.create(
        to=formatted_phone,
        code=code
    )
    return verification_check.status  # Returns 'approved' if correct

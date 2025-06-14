import os
from django.conf import settings
import razorpay

RAZORPAY_KEY_ID = 'rzp_test_AZyXvyZFBfF6TM'
RAZORPAY_KEY_SECRET = 'gORcC5u0p1fuYHtOmo9zyWmZ'

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
client.set_app_details({"title":"OneClick","version":"1.0"})
import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import json

# Load credentials from environment variables
load_dotenv()

# Fetch credentials securely
consumer_key = "5p3tv5lpVHOI3bBLrdKqQ2Q0k6a5BCAOJ3njutAz1uUPaRhJ"
consumer_secret = "zkgEbyJfs1KoRu62ApSdzSn0Zk8DpGFXJr1JfPHJ2YvL0iEIA9LpuFeVAJEoXeqk"
shortcode = "9357544 "
online_shortcode ="3077512"
lipa_secret = "lipa"

# API URLs
auth_url = "https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
stk_push_url = "https://api.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

# Function to get an access token
def get_access_token():
    response = requests.get(auth_url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        raise Exception("Error obtaining access token")

# Function to send an STK Push request
def send_stk_push(phone_number, amount):
    token = get_access_token()

    headers = {
        "Authorization": "Bearer " + token
    }

    payload = {
        "BusinessShortcode": online_shortcode,
        "LipaNaMpesaOnlineShortcode": online_shortcode,
        "PhoneNumber": phone_number,
        "Amount": amount,
        "AccountReference": "Test123",  # Reference for the transaction
        "TransactionDesc": "Payment for goods"  # Description of the transaction
    }

    response = requests.post(stk_push_url, json=payload, headers=headers)
    
    return response.json()

# Input from user
def main():
    phone_number = input("Enter the phone number (e.g., 2547XXXXXXXX): ")
    amount = float(input("Enter the amount: "))

    if not phone_number.startswith('254'):
        print("Invalid phone number format. Please enter a valid Kenyan phone number.")
        return

    print("Sending STK Push request...")
    result = send_stk_push(phone_number, amount)
    
    if result.get("ResponseCode") == "0":
        print(f"Payment request sent successfully! Checkout Request ID: {result.get('CheckoutRequestID')}")
    else:
        print(f"Error: {result.get('ResponseDescription')}")

if __name__ == "__main__":
    main()

import time
import csv
import requests
from twilio.rest import Client
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import playsound

#recovery code='SrmFlenkBq-rmZoxEReFS28I8EgQa6wA7CXrxael'
# Twilio API credentials
TWILIO_SID = 'AC5cd9b579f183619f91f531ca7be70e4a'
TWILIO_AUTH_TOKEN = '21a2ffa0593d84a582aebf75ecbf73b5'
TWILIO_PHONE_NUMBER = '+16207778677'
RECIPIENT_PHONE_NUMBER = '+916393168377'

# Email settings
EMAIL_SERVER = "smtp.gmail.com"
EMAIL_ADDRESS = 'badshahad001@gmail.com'
EMAIL_PASSWORD = 'Aayush@2811'
EMAIL_PORT = 587

API_ENDPOINT = "https://www.alphavantage.co/query"
API_KEY = '5F1ESCFPKC1B4S6P'


import csv
import requests

# Set the API endpoint and API key for getting stock data from Alpha Vantage


def update_target_prices(filename):
    # Read the stock data from the CSV file
    with open(filename, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        stocks = []
        for row in reader:
            stock = row["Stock"]
            stocks.append(stock)

    # Get the last day's highest price for each stock from the Alpha Vantage API
    target_prices = {}
    for stock in stocks:
        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": stock,
            "apikey": API_KEY
        }
        response = requests.get(API_ENDPOINT, params=params)
        data = response.json()
        last_day = list(data["Time Series (Daily)"].keys())[0]
        high = float(data["Time Series (Daily)"][last_day]["2. high"])
        target_prices[stock] = high

    # Update the target prices in the CSV file
    with open(filename, "w", newline="") as csvfile:
        fieldnames = ["Stock", "Target_Price"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for stock, target_price in target_prices.items():
            writer.writerow({"Stock": stock, "Target_Price": target_price})


def load_targets(filename):
    targets = {}
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            symbol, target_price = row
            targets[symbol] = float(target_price)
    return targets

# Fetch current stock prices using Alpha Vantage API
def get_live_stock_price(stock):
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": stock,
        "apikey": API_KEY
    }
    response = requests.get(API_ENDPOINT, params=params)
    data = response.json()
    return float(data["Global Quote"]["05. price"])

# Send SMS using Twilio
def send_sms(stock, target_price, current_price):
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        to=RECIPIENT_PHONE_NUMBER,
        from_=TWILIO_PHONE_NUMBER,
        body=f"Stock Alert: {stock} has reached target price of {target_price}. Current price is {current_price}."
    )

# Send email using SMTP
def send_email(stock, target_price, current_price):
    server = smtplib.SMTP(EMAIL_SERVER, EMAIL_PORT)
    server.starttls()
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    subject = f"Stock Alert: {stock} has reached target price of {target_price}"
    body = f"The current price of {stock} is {current_price}."
    message = f"Subject: {subject}\n\n{body}"
    server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, message)
    server.quit()




def play_sound():
    playsound('noti.mp3')

update_target_prices("price.csv")

with open("price.csv", newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    stocks = []
    for row in reader:
        stock = row["Stock"]
        target_price = float(row["Target_Price"])
        stocks.append((stock, target_price))

# Keep monitoring the live stock prices and send notifications when the stock price reaches the target price
while True:
    for stock, target_price in stocks:
        current_price = get_live_stock_price(stock)
        if current_price >= target_price:
            send_email(stock, target_price, current_price)
            send_sms(stock, target_price, current_price)
            play_sound()
            print(f"Stock Alert: {stock} has reached target price of {target_price}. Current price is {current_price}.")
            time.sleep(60) # Wait for 60 seconds before checking again
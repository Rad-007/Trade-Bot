import time
import pandas as pd
from jugaad_data.nse import NSELive
import playsound 
from twilio.rest import Client
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import yfinance as yf
from datetime import datetime, timedelta
from alpha_vantage.timeseries import TimeSeries



import yfinance as yf
import pandas as pd

# Function to set the target price to the previous day's max
def set_target_prices_to_previous_max(csv_filename):
    # Load the CSV file
    df = pd.read_csv(csv_filename)

    # Iterate through each row in the DataFrame
    for index, row in df.iterrows():
        stock = row['Stock']
        

        try:
            # Fetch historical data
            stock_data = yf.Ticker(stock)
            historical_data = stock_data.history(period="1d")

            if not historical_data.empty:
                # Find the maximum price for the previous day
                max_price = historical_data['High'].iloc[0]
                df.at[index, 'Target_Price'] = max_price
        except Exception as e:
            # Handle the exception (e.g., print an error message or skip the stock)
            print(f"Error fetching data for {stock}: {str(e)}")

    # Save the updated DataFrame back to the CSV file
    df.to_csv(csv_filename, index=False)

# Example usage:
csv_filename = 'price.csv'
set_target_prices_to_previous_max(csv_filename)


#set_target_prices_to_yesterdays_high('price.csv','5F1ESCFPKC1B4S6P')

print("Yesterday max set")









# Initialize NSELive
n = NSELive()

# Load the target prices from the CSV file
df = pd.read_csv('price.csv')



# Email settings


# Twilio credentials
twilio_account_sid = 'AC5cd9b579f183619f91f531ca7be70e4a'
twilio_auth_token = '21a2ffa0593d84a582aebf75ecbf73b5'
twilio_phone_number = '+16207778677'
recipient_phone_number = '+916393168377'

# Email credentials
EMAIL_SERVER = "smtp.gmail.com"
EMAIL_ADDRESS = 'badshahad001@gmail.com'
EMAIL_PASSWORD = 'Aayush@2811'
EMAIL_PORT = 587
'''
def send_email(stock, target_price, current_price):
    server = smtplib.SMTP(EMAIL_SERVER, EMAIL_PORT)
    server.starttls()
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    subject = f"Stock Alert: {stock} has reached target price of {target_price}"
    body = f"The current price of {stock} is {current_price}."
    message = f"Subject: {subject}\n\n{body}"
    server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, message)
    server.quit()
'''
import time
from pygame import mixer

def play_sound():
    mixer.init()
    mixer.music.load("noti.mp3")
    mixer.music.play()
    while mixer.music.get_busy():  # wait for music to finish playing
        time.sleep(1)

while True:
    for index, row in df.iterrows():
        stock = row['Stock']
        target_price = row['Target_Price']
        stock=stock.replace(".BSE","")
        q = n.stock_quote(stock)
        current_price = q['priceInfo']['lastPrice']

        if current_price >= target_price:
            # Send SMS
            client = Client(twilio_account_sid, twilio_auth_token)
            message = client.messages.create(
                body=f"{stock} reached the target price of {target_price}",
                from_=twilio_phone_number,
                to=recipient_phone_number
            )

            # Send email
            #send_email(stock, target_price, current_price)

            # Play sound notification
            print(f"{stock} reached the target price of {target_price}")
            #path=r"D:/Projects/Trade_Bot/Alert/noti.wav"
            play_sound()

    # Check every 60 seconds (adjust as needed)
    time.sleep(20)

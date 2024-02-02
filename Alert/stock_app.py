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

from predict_high_and_low import predict_high,predict_low

import yfinance as yf
import pandas as pd
predicted_price={}
predicted_low={}


# Predicted High price of stock
def get_predicted_high(csv_filename):
    
    df = pd.read_csv(csv_filename)

    # Iterate through each row in the DataFrame
    for index, row in df.iterrows():
        stock = row['Stock']
        price=predict_high(stock)
        predicted_price[stock]=round(price, 2)
    print("Predicted  High price of stocks",predicted_price)
    return(predicted_price)


# Predicted Low price of stock

def get_predicted_low(csv_filename):
    
    df = pd.read_csv(csv_filename)

    # Iterate through each row in the DataFrame
    for index, row in df.iterrows():
        stock = row['Stock']
        price=predict_low(stock)
        predicted_price[stock]=round(price, 2)
    print("Predicted Low  price of stocks",predicted_price)
    return(predicted_price)

    

# Function to set the target price to the previous day's max

def set_target_prices_to_previous_max(csv_filename):
    # Load the CSV file
    df = pd.read_csv(csv_filename)
    predicted_price=get_predicted_high(csv_filename)
    predicted_low=get_predicted_low(csv_filename)

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
                max_price=round(max_price, 2)
                price=predicted_price[stock]
                target_price=max(max_price,price)
                df.at[index, 'Target_Price'] = target_price

                low_price = historical_data['Low'].iloc[0]
                low_price=round(low_price, 2)
                price=predicted_low[stock]
                target_price=min(low_price,price)
                df.at[index, 'Buy_Price'] = target_price

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


#--------------------------------------------------------------------------------------------#


from api_testing import place_order

def buy(stock,price):
    place_order(stock,price,"BUY")

def sell(stock,price):
    place_order(stock,price,"SELL")



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


stocks_and_targets = df[['Stock', 'Target_Price','Buy_Price']].values.tolist()

import datetime
import time

# main  game starts here
start_time = datetime.time(hour=9, minute=0)  # 9:00 AM
end_time = datetime.time(hour=17, minute=0)  # 5:00 PM

while True:
    # Get the current time
    current_datetime = datetime.datetime.now()
    current_time = current_datetime.time()

    # Check if the current time is within the working hours
    if start_time <= current_time <= end_time:
        print("It's working hours. Do your work here.")
        buy_count=0
        sell_count=0
        while True:
            for stock, target_price,buy_price in stocks_and_targets:
                try:
                    # Create a Ticker object for the stock
                    stock_data = yf.Ticker(stock)

                    # Get the current live price (the 'Ask' price)
                    live_price = stock_data.info['ask']

                    print(f"{stock} live price is {live_price}")

                    # Compare the live price to the target price
                    if live_price >= target_price:
                        print(f"{stock} has reached the target price of {target_price} sell it")
                        if sell_count<1:
                            symbol=stock.replace(".NS","")
                            sell(symbol,target_price)
                            sell_count+=1
                        # Add your alerting code here (e.g., send SMS, email, sound notification)

                    if live_price <= buy_price:
                        print(f"{stock} has reached the buy price of {buy_price} buy it")
                        if buy_count<=1:
                            symbol=stock.replace(".NS","")
                            buy(symbol,buy_price)
                            buy_count+=1


                except Exception as e:
                    print(f"Error fetching data for {stock}: {str(e)}")
            
            time.sleep(10)
    else:
        
        print("It's outside of working hours. Waiting...")
    
    # Sleep for a while before checking the time again (e.g., every minute)
    time.sleep(3600) 


import csv
import requests
from io import StringIO
import json

from datetime import datetime

#Function to get data 
def stock_data():
    url = "https://uatopenapi.motilaloswal.com/getscripmastercsv?name=NSE"


    response = requests.get(url)
    csv_response = StringIO(response.text)
    csv_reader = csv.DictReader(csv_response)

    # Store the CSV data in a list of dictionaries
    csv_data = list(csv_reader)

    # Define the columns to extract and store in a CSV file
    columns_to_extract = ['exchange', 'exchangename', 'scripcode', 'scripshortname']

    # Store the selected columns in a new CSV file
    with open('stocks_NSE.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columns_to_extract)
        writer.writeheader()
        for row in csv_data:
            writer.writerow({key: row[key] for key in columns_to_extract})

    print("Done 👍")




# Function to get scripcode from scripshortname
def get_scripcode(scripshortname):
    with open('stocks_NSE.csv', 'r') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            if row['scripshortname'] == scripshortname:
                return row['scripcode']
    return None  # Return None if scripshortname is not found




# Test the get_scripcode function


'''
initial_url='http://uattrade.motilaloswal.com:83/OpenAPI/Login.aspx?apikey=jiFW05qWOUdwA58E'
response = requests.head(initial_url, allow_redirects=True)

# Get the final URL after following redirects
final_url = response.url

print("Initial URL:", initial_url)
print("Final URL:", final_url)
'''
def place_order_and_record_response(scripcode, buyorsell, price):
    # API URL for placing orders (use the appropriate URL for production or test)
    api_url = "	https://openapi.motilaloswal.com/rest/trans/v1/placeorder"

    TOTP='NIQMOSWNODVKAZMXMLJVNKR3FNG2P633'
    API_KEY='ccP5EcSw7uIR7AVw'
    AUTH='a2ca574c2d3d4f3b8164dd73831f37b4_M'

    # Prepare the request payload as a JSON object
    order_data = {
        "clientcode": "EMUM997001",  # Replace with your client code if needed
        "exchange": "NSE",  # Replace with the exchange name
        "symboltoken": int(scripcode),
        "buyorsell": buyorsell,
        "ordertype": "LIMIT",  # Modify as needed
        "producttype": "NORMAL",  # Modify as needed
        "orderduration": "DAY",  # Modify as needed
        "price": float(price),
        #"triggerprice": 0,  # Modify as needed
        "quantityinlot": 1,  # Modify as needed
        #"disclosedquantity": 0,  # Modify as needed
        "amoorder": "N",  # Modify as needed
        #"algoid": "",  # Modify as needed
        #"goodtilldate": "",  # Modify as needed
        #"tag": "",  # Modify as needed
        #"participantcode": ""  # Modify as needed
    }

    # Convert the order data to JSON format
    order_json = json.dumps(order_data)
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json', # Specify the expected response format
        'User-Agent': 'MOSL/V.1.1.0',  # Replace with your User-Agent
        'Authorization': AUTH,  # Replace with your Authorization token
        'ApiKey': API_KEY,  # Replace with your API Key
        'ClientLocalIp': '192.168.1.9',  # Replace with your local IP
        'ClientPublicIp': '110.225.254.109',  # Replace with your public IP
        'MacAddress': '6E-D3-2A-E8-9E-5F',  # Replace with your Mac Address
        'SourceId': 'WEB',  # Modify as needed
        'vendorinfo': 'T0240',  # Modify as needed
        'osname': 'Windows 10',  # Modify as needed
        'osversion': '10.0.19041',  # Modify as needed
        'devicemodel': 'AHV',  # Modify as needed
        'manufacturer': 'DELL',  # Modify as needed
        #'productname': 'Your Product Name',  # Modify as needed
        #'productversion': 'Your Product Version',  # Modify as needed
        #'installedappid': 'AppID',  # Modify as needed
        #'imeino': '15 Digit IMEI No.',  # Modify as needed
        #'browsername': 'Chrome',  # Modify as needed
        #'browserversion': '105.0'  # Modify as needed
    }
    # Send the POST request to place the order
    response = requests.post(api_url, data=order_json, headers=headers)

    # Create a timestamp for the current date and time
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Check the response
    if response.status_code == 200:
        response_data = response.json()
        response_message = response_data['message']
        unique_order_id = response_data.get('uniqueorderid', '')

        print(response_data)

        # Store the response in a CSV file with the timestamp
        with open(f"order_response.csv", mode='a', newline='') as file:
            writer = csv.writer(file)
            #writer.writerow(['Timestamp', 'Scripcode', 'BuyorSell', 'Price', 'Response Message', 'Order ID'])
            writer.writerow([timestamp, scripcode, buyorsell, price, response_message, unique_order_id])

        return True, response_message, unique_order_id
    else:
        return False, f"Failed to place order. HTTP Status Code: {response.status_code}", None

# Example usage:




def place_order(stock,price,buyorsell):
    scrip_code = get_scripcode(stock)


    # Replace with your scrip code
    buy_or_sell = buyorsell  # Replace with BUY or SELL
    order_price = price  # Replace with your order price

    success, message, order_id = place_order_and_record_response(scrip_code, buy_or_sell, order_price)

    if success:
        print(f"Order placed successfully. Order ID: {order_id}")
    else:
        print(f"Order placement failed. Message: {message}")



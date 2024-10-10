# This program will inform the user about the availibility of a product in amazon online shopping website.

import random
import requests
import schedule
import logging
from time import sleep
from lxml import html



# Logging levels in python, sorted in increasing order based on severity: Debug, Info, Warning, Error, Critical
# By setting the level to Info, the logging system handles all messages that are at the Info level or higher.
# %(asctime)s displayes the time when the log message was created.

# Configure logging
logging.basicConfig( level=logging.INFO, format= '%(asctime)s - %(levelname)s - %(message)s')

def check(url):
    header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
    try:
        response = requests.get(url, headers=header, timeout=10)
        logging.info(f"Response status code: {response.status_code}")
        response.raise_for_status()
        info = html.fromstring(response.content)

        # to check the availability
        availability = info.xpath('//div[@id ="availability"]//text()')
        return ''.join(availability).strip()

    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occured: {http_err}")

    except requests.exceptions.ConnectionError as con_err:
        logging.error(f"Connection error occured: {con_err}")

    except requests.exceptions.Timeout as timeout:
        logging.error(f"Timeout error occured: {timeout}")

    except requests.exceptions.RequestException as req_ex:
        logging.error(f"Request error occured: {req_ex}")

    return None

def monitor_availability():
    url = ask_user

    logging.info(f"Checking the availability for {url}")
    availability_status = check(url)

    if availability_status:
        logging.info(f"Status: {availability_status}")

        if "In stock" in availability_status:
            logging.info("The product is available")

        elif "Temporarily Out of Stock" in availability_status or "Currently unavailable" in availability_status:
            logging.info("The product is not available.")

        elif "Only" in availability_status and "left in stock" in availability_status:
           logging.info("The product is available but only a limited quantity is left")
            
    else:
        logging.warning("Failed to retrieve information about availability status.")

print("---- Product Availability Checker (Amazon) ----\n")
ask_user = input("Please enter link of the product: ") # Example: https://amzn.eu/d/g9PIiD1
schedule.every(1).minutes.do(monitor_availability)

while True:
    schedule.run_pending()
    sleep(random.uniform(5, 15))  # Reduced sleep time

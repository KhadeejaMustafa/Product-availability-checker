# This program will inform the user about the availibility to a product in an online shopping website.
import random
import requests
import schedule
from time import sleep
from lxml import html

def check(url):
    header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
    try:
        response = requests.get(url, headers=header, timeout=10)
        print(f"Response status code: {response.status_code}")
        response.raise_for_status()
        info = html.fromstring(response.content)

        # to check the availability
        availability = info.xpath('//div[@id ="availability"]//text()')
        return ''.join(availability).strip()

    except requests.exceptions.RequestException as e:
        print(f"Error while checking availability: {e}")
        return None

def monitor_availability():
    url = f"https://www.amazon.com/GODONLIF-Candle-Adjustable-Dimmable-Candles/dp/B0CTJGJL2T"

    print(f"Checking the availability for {url}")
    availability_status = check(url)

    if availability_status:
        print(f"Status: {availability_status}")

        if "In Stock" in availability_status or "Only" in availability_status:
            print("The product is available")
        else:
            print("Product is not available")
    else:
        print("Failed to retrieve information about availability status")

schedule.every(1).minutes.do(monitor_availability)

while True:
    schedule.run_pending()
    sleep(random.uniform(5, 15))  # Reduced sleep time

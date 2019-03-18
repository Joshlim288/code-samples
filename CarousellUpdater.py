
import requests
from bs4 import BeautifulSoup
import webbrowser
import time
from datetime import datetime


def save_html(html, path):
    with open(path, 'wb') as i:
        i.write(html)


def open_html(path):
    with open(path, 'rb') as i:
        return i.read()

# Variables
url = 'https://sg.carousell.com/search/products/?sort_by=time_created%2Cdescending&query=nintendo%20switch%20games&cc_id=412'
delay = 5 # in minutes

# Get current first sale
print('Getting data...\n')
r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')
current_first_sale = soup.select_one('.G-ab').text.strip()

# Check page
while True:
    # save pages
    print('Refreshing...\n')
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    new_first_sale = soup.select_one('.G-ab').text.strip()
    if new_first_sale != current_first_sale:
        break
    print('{}: No new updates\n'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    time.sleep(delay*60)

url = 'https://sg.carousell.com' + new_first_sale['href']
webbrowser.open(url)

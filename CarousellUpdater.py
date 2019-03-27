
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
    
# check = input('close script when new listing found?').upper()
check = 'N'
print('Getting data...\n')

while True:
    # Variables
    url = 'https://sg.carousell.com/search/products/?cc_id=412&query=nintendo%20switch%20&sort_by=time_created%2Cdescending'
    delay = 5 # in minutes

    # Get current first sale
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    selector = '.' + soup.select_one('a[class$="-ab"]')['class'][0]
    current_first_sale = soup.select_one(selector)

    # Check page
    while True:
        # save pages
        print('Refreshing...\n')
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        new_first_sale = soup.select_one(selector)
        if new_first_sale.text.strip() != current_first_sale.text.strip():
            print('New listing found!')
            print('Opening web page...')
            break
        print('{}: No new updates\n'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        time.sleep(delay*60)

    url = 'https://sg.carousell.com' + new_first_sale['href']
    webbrowser.open(url)
    if check == 'Y':
        break
    

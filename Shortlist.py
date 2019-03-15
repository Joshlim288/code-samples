# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 22:28:36 2019
@author: Josh
"""

import requests
from bs4 import BeautifulSoup
import xlsxwriter
import time


def get_soup(url):
    r = requests.get(url)
    return BeautifulSoup(r.content, 'html.parser')


def write_xlsx(items, xlsx_write_row):
    write_column = 0
    for item in items:
        worksheet.write(xlsx_write_row, write_column, item)
        write_column += 1


workbook = xlsxwriter.Workbook('Results.xlsx')
worksheet = workbook.add_worksheet()


# user variables
while True:
    start_url = input('Start url: ')
    if 'https://www.tripadvisor.com.sg/Hotels-' not in start_url:
        print('Please enter a valid url. e.g https://www.tripadvisor.com.sg/Hotels-g255100-Melbourne_Victoria-Hotels.html')
    else:
        break

print('fetching page...')
soup = get_soup(start_url)

while True:
    min_rev_num = input('Min Reviews for property: ')
    if min_rev_num.isdigit():
        if int(min_rev_num) >= 0:
            min_rev_num = int(min_rev_num)
            break
    print('Please enter a valid number')

while True:
    print('Enter max number of low review number properties on a single page, from 0 to 30')
    print('(Program will exit once this condition is fulfilled)')
    num_rev_criteria = input('Input: ')
    if num_rev_criteria.isdigit():
        if 0 <= int(num_rev_criteria) <= 30:
            num_rev_criteria = int(num_rev_criteria)
            break

    print('Please enter a valid number')

while True:
    min_star_rating = input('Min star rating for property: ')
    if min_star_rating.isdigit():
        if 0 <= int(min_star_rating) <= 5:
            min_star_rating = float(min_star_rating)
            break

    print('Please enter a valid number')

while True:
    min_room_num = input('Min number of rooms: ')
    if min_room_num.isdigit():
        if int(min_room_num) >= 0:
            min_room_num = int(min_room_num)
            break
    print('Please enter a valid number')

while True:
    max_num_pages = int(soup.select_one('.pageNum.last.taLnk').text.strip())
    num_pages = input('Page to search until(1 to {}):'.format(str(max_num_pages)))
    if num_pages.isdigit():
        if 1 <= int(num_pages) <= max_num_pages:
            num_pages = int(num_pages)
            break
    print('Please enter a valid number')
print('-'*30 + '\n')
check = input("\nMake sure 'Results.xlsx' is closed and deleted. Once you are ready, press enter")

write_row = 0
write_xlsx(['Property Details', 'Star Rating', 'Number of Rooms'], write_row)
page_url = start_url
rejected_properties = 0

start = time.time()
print('Getting data...')

# get property data
for page_num in range(num_pages):
    print('\nOn page {}'.format(str(page_num + 1)))
    low_review_count = 0
    soup = get_soup(page_url)
    if page_num != num_pages - 1:
        next_page = soup.select_one('.nav.next.taLnk.ui_button.primary')['href']
        page_url = 'https://www.tripadvisor.com.sg' + next_page
    else:
        pass
    rows = soup.select('.property_title.prominent')
    prop_urls = []
    for row in rows:
        prop_urls.append('https://www.tripadvisor.com.sg' + row['href'])
    for prop in prop_urls:
        soup = get_soup(prop)
        try:
            num_reviews = int(soup.select_one('.reviewCount').text.strip().split(' ')[0].replace(',', ''))
        except AttributeError:
            num_reviews = 0

        try:
            property_name = soup.select_one('#HEADING').text.strip()
        except AttributeError:
            property_name = ' '
            
        if num_reviews >= min_rev_num:

            try:
                star_rating_class = soup.select_one('.ui_star_rating')['class'][1]
                star_rating = float(star_rating_class[5] + '.' + star_rating_class[6])
            except TypeError:
                star_rating = 0

            num_rooms = 0
            extra_info = soup.select('.hotels-hotel-review-about-addendum-AddendumItem__content--iVts5')
            for data in extra_info:
                data = data.text.strip()
                if data.isdigit():
                    num_rooms = int(data)

            try:
                address = soup.select_one('.street-address').text.strip() + ', ' + soup.select_one('.locality').text.strip() + soup.select_one('.country-name').text.strip()
            except AttributeError:
                address = ' '

            try:
                phone = soup.select_one('.is-hidden-mobile.detail').text.strip()
            except AttributeError:
                phone = ' '

            if star_rating >= min_star_rating or star_rating == 0:
                if num_rooms >= min_room_num or num_rooms == 0:
                    write_row += 1
                    write_xlsx([property_name + '\n' + address + '\nT: ' + phone, star_rating, num_rooms], write_row)
                else:
                    print("\nRejected: '{}'\n".format(property_name) + ' - Not enough rooms: {}'.format(num_rooms))
            else:
                print("\nRejected: '{}'\n".format(property_name)+' - Not high enough star rating: {}'.format(star_rating))
        else:
            low_review_count += 1
            print("\nRejected: '{}'\n".format(property_name) + ' - Not enough reviews: {}'.format(num_reviews))
            print(' - Low review count: {}/{}'.format(low_review_count, num_rev_criteria))

    if low_review_count >= num_rev_criteria:
        print('\nExiting due to low review count on page')
        break
    
workbook.close()
end = time.time()

print("\nDone! Results can be found in 'Results.xlsx' in the same folder\n")
print('Results can be copied straight onto the shortlist(paste values only), formatting has already been done.')
print('If any results have 0 stars or 0 rooms, They have to be found manually.')
print('Address and phone numbers are based on Tripadvisor data as well\n')
print('Number of pages searched: {}'.format(str(page_num + 1)))
props_searched = (page_num)*30
print('Number of properties searched: {}'.format(str(props_searched)))
print('Number of properties accepted: {}'.format(str(write_row - 1)))
print('Number of properties rejected: {}'.format(str(props_searched - write_row + 1)))
print('Time taken: {} minutes'.format(str((end-start)//60)))
while True:
    check = input('\nTo exit, press enter')
    if True:
        break


'''
Notes:
1) Will still get data if any of the parameters are missing,
   as long as the parameters that do exist meet the criteria
2) Current break criteria is for a page to have a certain number
   of entries with low reviews. This can be changed to suit needs.
3) This scraper relies on data from tripadvisor, which might not
   have much info on hotels in some destinations, like China.
4) Address and phone number are taken from tripadvisor as well.
   If you require time/dist to airport, and address/phone from google,
   must be done manually. Google maps does not allow these pages to
   be scraped.
5) Indiscriminate searching(no min num of reviews) will take 
   around 1min per page
6) Sometimes, some properties may show 0 rooms or 0 stars even though they fulfill
   the criteria. It is recommended to check all properties that show they have
   0 rooms
7) When copying results to shortlist file, paste values only. If you want
   to bold the property names, use the included macro 'boldfirstline.bas'.
   import it into the shortlist excel sheet and run it.
8) ***Make sure not to have results.xlsx open while running this script.***
ToDo:
1) Replace try and excepts with something less problematic
2) include vba script for formatting
3) Get inputs  through tkinter
4) Work on efficiency*
5) Replace num_rooms selector. It contains a random string that needs to be updated anytime tripadvisor recieves and update.
  - The #id div div div div div selector is very slow, find an alternative
'''

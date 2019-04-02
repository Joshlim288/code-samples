# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 22:28:36 2019
@author: Josh
"""

import requests
from bs4 import BeautifulSoup
import xlsxwriter
import time


def get_selector(html_soup):
    selector_list = html_soup.select('div[class^="hotels-hotel-review-about-addendum-AddendumItem__content--"]')
    for div in selector_list:
        if div.text.strip().isdigit():
            selector = '.' + div['class'][0]
            return selector
    return ''


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
rooms_selector = ''
total_properties = 0

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
    try:
        min_star_rating = float(min_star_rating)
        if 0 <= float(min_star_rating) <= 5:
            break
    except ValueError:
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

while True:
    keep_props = input('Do you want to include properties with missing number of rooms/star rating?(Y/N)')
    if keep_props.isalpha():
        if keep_props.upper() == 'Y' or keep_props.upper() == 'N':
            break
    print('Please enter a valid response')


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
        total_properties += 1
        soup = get_soup(prop)
        num_reviews = 0
        property_name = ''
        star_rating = 0
        num_rooms = 0
        extra_info = []
        star_rating_class = 0
        address = ' '
        phone = ' '
        attempt = 0
        while True:
            try:
                num_reviews = int(soup.select_one('.reviewCount').text.strip().split(' ')[0].replace(',', ''))
            except AttributeError:
                num_reviews = 0
            if attempt > 1 or num_reviews != 0:
                break
            else:
                soup = get_soup(prop)
                attempt += 1

        try:
            property_name = soup.select_one('#HEADING').text.strip()
        except AttributeError:
            property_name = ' '
            
        if num_reviews >= min_rev_num:
            # star rating
            while True:
                try:
                    star_rating_class = soup.select('.ui_star_rating')
                    for index in range(len(star_rating_class)):
                        star_rating_class[index] = star_rating_class[index]['class']
                except TypeError:
                    star_rating = 0
                # fix this part
                if star_rating_class != 0:
                    for lst in star_rating_class:
                        for item in lst:
                            if 'cross-sells-items-grid-comparisons-Icon__icon' in item:
                                star_rating = 'wrong star rating'
                                break
                        if star_rating == 'wrong star rating':
                            star_rating = 0
                        else:
                            star_rating = float(lst[1][5] + '.' + lst[1][6])
                            break
                if attempt > 1 or star_rating != 0:
                    break
                else:
                    soup = get_soup(prop)
                    attempt += 1

            attempt = 0

            # num rooms
            while True:
                if not rooms_selector:
                    rooms_selector = get_selector(soup)
                    
                if not rooms_selector:
                    num_rooms = 0
                else:
                    extra_info = soup.select(rooms_selector)
                    if not extra_info:
                        extra_info = soup.select('.textitem')
                    for data in extra_info:
                        data = data.text.strip()
                        if data.isdigit():
                            num_rooms = int(data)

                if attempt > 1 or num_rooms != 0:
                    break
                else:
                    soup = get_soup(prop)
                    attempt += 1

            # address
            try:
                address = soup.select_one('.street-address').text.strip() + ', ' + soup.select_one('.locality').text.strip() + soup.select_one('.country-name').text.strip()
            except AttributeError:
                address = ' '

            # phone
            try:
                phone = soup.select_one('.is-hidden-mobile.detail').text.strip()
            except AttributeError:
                phone = ' '

            # Check conditions, write to xl
            if keep_props.upper() == 'Y':
                if star_rating >= min_star_rating or star_rating == 0:
                    if num_rooms >= min_room_num or num_rooms == 0:
                        write_row += 1
                        write_xlsx([property_name + '\n' + address + '\nT: ' + phone, star_rating, num_rooms], write_row)
                    else:
                        print("\nRejected: '{}'\n".format(property_name) + ' - Not enough rooms: {}'.format(num_rooms))
                else:
                    print("\nRejected: '{}'\n".format(property_name)+' - Not high enough star rating: {}'.format(star_rating))

            else:
                if star_rating >= min_star_rating:
                    if num_rooms >= min_room_num:
                        write_row += 1
                        write_xlsx([property_name + '\n' + address + '\nT: ' + phone, star_rating, num_rooms], write_row)
                    elif num_rooms == 0:
                        print("\nRejected: '{}'\n".format(property_name) + ' - Information missing: Number of rooms')
                    else:
                        print("\nRejected: '{}'\n".format(property_name) + ' - Not enough rooms: {}'.format(num_rooms))
                elif star_rating == 0:
                    print("\nRejected: '{}'\n".format(property_name) + ' - information missing: Star rating')
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
if keep_props.upper() == 'Y':
    print('If any results have 0 stars or 0 rooms, Tripadvisor does not have the data. \nThey have to be found manually.')
print('Address and phone numbers are based on Tripadvisor data as well\n')
print('Number of pages searched: {}'.format(str(page_num + 1)))
print('Number of properties searched: {}'.format(str(total_properties)))
print('Number of properties accepted: {}'.format(str(write_row)))
print('Number of properties rejected: {}'.format(str(total_properties - write_row)))
m, s = divmod((end-start), 60)
h, m = divmod(m, 60)
print('Time Taken: {:d}:{:02d}:{:02d}'.format(int(h), int(m), int(s)))
input('\nPress enter to close the program')



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
4) eliminate duplicates
5) create example sheet
'''

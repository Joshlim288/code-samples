# -*- coding: utf-8 -*-
"""
Created on Thu Jan 24 20:51:32 2019

@author: Josh
"""

import requests
from bs4 import BeautifulSoup
import csv


def save_html(html, path):
    with open(path, 'wb') as f:
        f.write(html)


def open_html(path):
    with open(path, 'rb') as f:
        return f.read()

def write_csv(items)
    with open('Shortlist.csv', 'a') as shortlist:
        property_writer = csv.writer(shortlist)
        property_writer.writerow(items)

# user variables
start_url = 'https://www.tripadvisor.com.sg/Hotels-g255100-Melbourne_Victoria-Hotels.html'
num_rev_criteria = 7
min_rev_num = 100
min_star_rating = 4
min_room_num = 90

# get num pages
r = requests.get(start_url)
save_html(r.content, 'page')
soup = BeautifulSoup(open_html('page'), 'html.parser')
num_pages = int(soup.select_one('.pageNum.last.taLnk').text.strip())
write_csv(['Property Name', 'Star Rating', 'Number of Rooms', 'Address', 'Contact Number'])

# get property data
for page_num in range(num_pages):
    low_review_count = 0
    rows = soup.select('.property_title.prominent')
    prop_urls = []
    for row in rows:
        prop_urls.append('https://www.tripadvisor.com.sg' + row['href'])
    for property in prop_urls:
        r = requests.get(property)
        save_html(r.content, 'page')
        soup = BeautifulSoup(open_html('page'), 'html.parser')
        num_reviews = int(soup.select_one('.reviewCount').text.strip())
        if num_reviews >= min_rev_num:
            try:
                property_name = soup.select_one('#HEADING').text.strip()
            except TypeError:
                property_name = ' '

            try:
                star_rating_class = soup.select_one('.hotels-hotel-review-about-with-photos-layout-TextItem__textitem--3CMuR span')['class']
                star_rating = int(star_rating_class[19] + '.' + star_rating_class[20])
            except TypeError:
                star_rating = 0

            try:
                num_rooms = int(soup.select_one('.hotels-hotel-review-about-addendum-AddendumItem__content--28NoV').text.strip())
            except TypeError:
                num_rooms = 0

            try:            
                address = soup.select_one('.street-address').text.strip() + ', ' + soup.select_one('.locality').text.strip() + ', ' + soup.select_one('.country-name').text.strip()
            except TypeError:
                address = ' '
            
            try:            
                phone = soup.select_one('.is-hidden-mobile.detail').text.strip()
            except TypeError:
                phone = ' '

            if star_rating >= min_star_rating or star_rating == 0:
                if num_rooms >= min_room_num or num_rooms == 0:
                    write_csv([property_name, str(star_rating), str(num_rooms), address, phone])
        else:
            low_review_count += 1
    next_page = soup.select_one('.nav.next.taLnk.ui_button.primary')['href']
    page_url = 'https://www.tripadvisor.com.sg' + next_page
    r = requests.get(page_url)
    save_html(r.content,'page')
    soup = BeautifulSoup(open_html('page'), 'html.parser')
    if low_review_count > rev_criteria:
        break




'''
ToDo:


'''

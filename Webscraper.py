# -*- coding: utf-8 -*-
"""
Created on Thu Jan 24 20:51:32 2019

@author: Josh
"""

import requests
from bs4 import BeautifulSoup


def save_html(html, path):
    with open(path, 'wb') as f:
        f.write(html)


def open_html(path):
    with open(path, 'rb') as f:
        return f.read()


try:
    soup = BeautifulSoup(open_html('steam'), 'html.parser')
    old_steam_sales = soup.select_one('.search_pagination_left').text.strip().split(' ')[5] # number
except FileNotFoundError:
    old_steam_sales = '0'


try:
    soup = BeautifulSoup(open_html('ubi'), 'html.parser')
    old_ubi_sales = soup.select_one('.results-hits p span').text.strip().split(' ')[0] # number
except FileNotFoundError:
    old_ubi_sales = '0'


try:
    soup = BeautifulSoup(open_html('humble'), 'html.parser')
    old_num_bundles = soup.select_one('.js-bundle-dropdown.js-navbar-dropdown.button-title').text.strip() # 8 bundles
except FileNotFoundError:
    old_num_bundles = '0 bundles'


try:
    soup = BeautifulSoup(open_html('bookwalker'), 'html.parser')
    old_bw_sales = soup.select_one('.result-page-num').text.strip().split(' ')[2] # number
except FileNotFoundError:
    old_bw_sales = '0'


try:
    soup = BeautifulSoup(open_html('comixology'), 'html.parser')
    titles = soup.select('.list-title')
    old_com_headers = [title.text.strip() for title in titles] # list of titles 'title (222 items)'
except FileNotFoundError:
    old_titles = []



# save pages

print('Getting data...')
url = 'https://store.steampowered.com/search/?specials=1&os=win'
r = requests.get(url)
save_html(r.content, 'steam')

url = 'https://store.ubi.com/sea/deals?lang=en_SG'
r = requests.get(url)
save_html(r.content, 'ubi')

url = 'https://www.humblebundle.com/store/search?sort=discount&filter=onsale'
r = requests.get(url)
save_html(r.content, 'humble')


url = 'https://global.bookwalker.jp/search/?qspp=1&np=1&order=title/'
r = requests.get(url)
save_html(r.content, 'bookwalker')


url = 'https://www.comixology.com/comics-sale'
r = requests.get(url)
save_html(r.content, 'comixology')



# Get new data
soup = BeautifulSoup(open_html('steam'), 'html.parser')
steam_sales = soup.select_one('.search_pagination_left').text.strip().split(' ')[5] # number
if steam_sales != old_steam_sales:
    steam_sales += '*'

soup = BeautifulSoup(open_html('ubi'), 'html.parser')
ubi_sales = soup.select_one('.results-hits p span').text.strip().split(' ')[0] # number
if ubi_sales != old_ubi_sales:
    ubi_sales += '*'

soup = BeautifulSoup(open_html('humble'), 'html.parser')
num_bundles = soup.select_one('.js-bundle-dropdown.js-navbar-dropdown.button-title').text.strip() # 8 bundles
if num_bundles != old_num_bundles:
    num_bundles += '*'


soup = BeautifulSoup(open_html('bookwalker'), 'html.parser')
bw_sales = soup.select_one('.result-page-num').text.strip().split(' ')[2] # number
if bw_sales != old_bw_sales:
    bw_sales += '*'


soup = BeautifulSoup(open_html('comixology'), 'html.parser')
titles = soup.select('.list-title')
com_headers = [title.text.strip() for title in titles] # list of titles 'title (222 items)'
for i in range(len(com_headers)):
    if com_headers[i] not in old_com_headers:
        com_headers[i] += '*'
    com_headers[i] = str(i+1) + ') ' + com_headers[i]
    


msg = ('\n'*2 + ' '*4 + 'Sales\n' + '-'*13 + 
       '\n\nAny changes to the sales will be reflected by an asterisk next to it' +
       '\nThese results will be written to the Sales file in the same directory' +
       '\n\nGames:'
       '\n\nSteam: {} games on sale'.format(steam_sales) +
       '\n\nUplay: {} games on sale'.format(ubi_sales) +
       '\n\nHumble Bundle: {}'.format(num_bundles) +
       '\n\n\nBooks:'
       '\n\nBookwalker: {} books on sale'.format(bw_sales) +
       '\n\nComixology: {} sales ongoing'.format(str(len(com_headers))) +
       '\n\nTitle of Comixology sales:\n')

with open('Sales.txt', 'w') as f:
    print(msg)
    f.write(msg + '\n')
    for header in com_headers:
        print(header)
        f.write(header + '\n'*2)


'''
ToDo list:
1) Get number of sales from humblebundle(its rendered in js) using selenium
2) Efficiency, especially for the headers part
3) Get titles of humble bundle sales
4) Add wishlist
5) Add links to website
6) fix so that if the same number but different sales still works
'''
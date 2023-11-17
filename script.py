#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
import sqlite3
from sqlite3 import Error


def insert(con, link,site,nick, age):
        try:
             cur = con.cursor()
             cur.execute("INSERT INTO house VALUES(?,?,?,?)",(link,site,nick,age))
             con.commit()
        except Error as e:
            print(f"The error '{e}' occurred")

def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

def scrapSite(number):
    
    s = requests.session()

    con = s.get(f'https://pl.escort.club/anonse/towarzyskie/poznan/page{number}.html?province=30&district=&filter_price_type=&filter_price=0%3B25000&filter_age=18%3B100&filter_weight=30%3B200&filter_height=100%3B220&filter_breasts=0%3B8&breasts_type=&hair_colors=&sexual_orientation=&searchlang=&zodiac_sign=&q=')

    soup = BeautifulSoup(con.text)
    con = create_connection('bigdb.db')



    links = soup.find_all("div", "item-col col")

    print(len(links))

    for tag in links:
        tags = tag.find_all("a")
        for t1 in tags:
            if t1['href'] != '#':
                link = t1['href']
                info = t1.find_all('span','item-info')
                nick = t1.find_all('span','item-name')
                siteTag = t1.find_all('span','item-stats')

                age = siteTag[0].text.split(',')[1][:-1]
                site = siteTag[0].text.split(',')[0]
            
                insert(con,link, site,nick[0].text, age)
                print('add to db...')


for x in range(8):
    scrapSite(x+1)

print("Date execute!")


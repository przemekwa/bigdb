#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
import sqlite3
from sqlite3 import Error
import re
import matplotlib.pyplot as plt



count = 1

def insert(con, link,site,nick, age,price,weight, height):
        try:
             cur = con.cursor()
             cur.execute("INSERT INTO house VALUES(?,?,?,?,?,?,?)",(link,site,nick,age,price,weight, height))
             con.commit()
        except Error as e:
            print(f"The error '{e}' occurred")

def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        #print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

def getIntFromString(str):
    parseInt = re.findall(r'\d+', str)
    if len(parseInt) > 0:
        return parseInt[0]
    else:
        return -1 

def select_all_tasks(conn):
   
    cur = conn.cursor()
    cur.execute("select age, count(*) from (select max(link), price,  height,age from house where site='Poznań' group by price,  height,age) group by age order by count(*);")

    rows = cur.fetchall()

    ages = []
    counts = []

    for row in rows:
        ages.append(f'{row[0]}')
        counts.append(f'{row[1]}')

    fig, ax = plt.subplots()
    ax.bar(ages,counts)
    ax.set_title('Fruit supply by kind and color')
    plt.savefig('temp.png')
        
def scrapSite(number):
    global count
    s = requests.session()





    con = s.get(f'https://pl.escort.club/anonse/panie/poznan/page{number}.html?province=30&district=&filter_price_type=&filter_price=0%3B25000&filter_age=18%3B100&filter_weight=30%3B200&filter_height=100%3B220&filter_breasts=0%3B8&breasts_type=&hair_colors=&sexual_orientation=&searchlang=&zodiac_sign=&q=')

    soup = BeautifulSoup(con.text)
    con = create_connection('bigdb1.db')

    links = soup.find_all("div", "item-col col")

    for tag in links:
        aTags = tag.find_all("a")
        for aTag in aTags:
            if aTag['href'] != '#':
                link = aTag['href']
                info = aTag.find_all('span','item-info')
                nick = aTag.find_all('span','item-name')
                stats = aTag.find_all('span','item-stats')
                age = stats[0].text.split(',')[1][:-1]
                site = stats[0].text.split(',')[0]
        other = tag.find_all('span','item-info -bottom')[0].find_all('span','-title')
        price = getIntFromString(other[0].text)
        weight = getIntFromString(other[4].text)
        height = getIntFromString(other[5].text)
        print(f'{count} - add to db ...')
        count = count+1
        insert(con,link, site,nick[0].text, age, price,weight, height)

count = count+1
for x in range(8):
    scrapSite(x+1)

#con = create_connection('bigdb1.db')
# date = select_all_tasks(con)

print("Date execute!")


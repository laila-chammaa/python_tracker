import requests
from bs4 import BeautifulSoup
import smtplib
import time
from config import *

#hiding sensitive info in the config file, so from_email, to_email and a password

URL = 'https://www.amazon.ca/Dell-UltraSharp-U2417H-LED-Monitor/dp/B01IRRGH7M/ref=sr_1_1?crid=1337C0HOHBMCO&dchild=1&keywords=dell+monitor+24+U2417H&qid=1599350489&sprefix=dell+moni%2Caps%2C164&sr=8-1'

wanted_price = 250;

headers = {"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15'}

def check_price():
    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')
    #soup = BeautifulSoup(page.content,'lxml') # <-- change to 'lxml' or 'html5lib'\
    soup = BeautifulSoup(page.content, "html5lib")

    title = soup.find(id='productTitle').get_text().strip()
    price = soup.find(id='priceblock_ourprice').get_text().strip()
    converted_price = float(price[4:8])

    if(converted_price > wanted_price):
        send_mail()

    print(title)
    print(converted_price)


def send_mail():
    #establishing a connection between this app and our gmail
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    #encripting our connection
    server.starttls()
    server.ehlo()
    #email and password
    server.login(from_email, password)
    subject = 'python tracker: price went down on the dell monitor'
    body = 'check the amazon link: ' + URL
    msg = "Subject: " + subject + "\n\n" + body

    #first arg: from, second: to, third: actual message
    server.sendmail(from_email, to_email, msg)
    print('HEY EMAIL SENT')
    server.quit()

while (True):
    check_price()
    #checks once a week
    time.sleep(604800)
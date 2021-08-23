import tweepy as tp
import credential
from bs4 import BeautifulSoup
import requests
import time
from datetime import datetime

auth = tp.OAuthHandler(credential.API_key, credential.API_secret_key)
auth.set_access_token(credential.access_token, credential.access_token_secret)
api = tp.API(auth)

try:
    api.verify_credentials()
    print("Authentication Successful")

except:
    print("Authentication Error")

URL= 'https://www.iccuk.org'

page= requests.get(URL)

soup = BeautifulSoup(page.text, 'lxml')

prayer = soup.find('div', {'id': 'adWrapPrayTimesCol1'})
prayer = prayer.find_all('p')

pray=[] 
for row in prayer:
    pray.append(row.text)

table = soup.find('div', {'id': 'adWrapPrayTimesCol2'})
table = table.find_all('p')

times = []
for t in table:
    times.append(t.text)

prayer_times= {}

for index in range(0,len(times)):
    if index < 2:
        times[index]= datetime.strptime(times[index]+' AM', '%I.%M %p').strftime('%H:%M')
    elif index == 2: 
        if times[index] < times[index+1]:
            times[index] = datetime.strptime(times[index]+' PM', '%I.%M %p').strftime('%H:%M')
        elif times[index] > times [index+1]:
            times[index] = datetime.strptime(times[index]+' AM', '%I.%M %p').strftime('%H:%M')
    elif index > 2:
        times[index]= datetime.strptime(times[index]+' PM', '%I.%M %p').strftime('%H:%M')

prayer_times={}

for index in range(0, len(times)):
    prayer_times[times[index]]=pray[index]

# prayer_times['18:11']='asr'
now = time.strftime('%H:%M')

if now in prayer_times.keys():
    api.update_status('It is now the prayer time for ' + prayer_times[now] +' at ' + now + ' according to London local time')
    # print('It is now the prayer time for ' + prayer_times[now] +' at ' + now + ' according to London local time')
# api.update_status('Assalmualai')


import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import time

visit_data = pd.read_csv('foursquare-nyc-and-tokyo-check-ins/dataset_TSMC2014_TKY.csv', nrows=227429)
visit_data2 = pd.read_csv('foursquare-nyc-and-tokyo-check-ins/dataset_TSMC2014_NYC.csv', nrows=227429)

visit_data.head()
visit_data.sort_values('userId')
sorted_by_user = visit_data.sort_values(by=['userId', 'utcTimestamp'])

sorted_by_user['utcTimestamp'] = pd.to_datetime(sorted_by_user['utcTimestamp'], infer_datetime_format=True)
sorted_by_user2 = sorted_by_user.sort_values(by=['userId', 'utcTimestamp'])
sorted_by_user2['utcTimestamp'] = sorted_by_user2['utcTimestamp'].dt.tz_localize('UTC').dt.tz_convert('Asia/Tokyo')

sorted_by_user['utcTimestamp'] = pd.to_datetime(sorted_by_user['utcTimestamp'], format='%a %b %d %H:%M:%S %z %Y')
datetime.datetime.strptime('Fri Jan 15 11:01:21 +0000 2012', '%a %b %d %H:%M:%S %z %Y')

# from mpl_toolkits.basemap import Basemap
# map = Basemap()
#
# map.drawcoastlines()

import foursquare

import json, requests


def get_venue_info(venueID, date, latitude, longitude, query_category):
    url = 'https://api.foursquare.com/v2/venues/' + venueID

    params = dict(
      client_id='JPSTZ2VV3CWLLIVYWCW3TK4ML0PTLY23IL15BNZ03MEK5MNL',
      client_secret='RAKHEUG0HM4LCGZ0IFDTV4SGL0D1PIVC1H03R5JEYSPWOWCA',
      v=date,
      ll=str(latitude) + ',' + str(longitude),
      query=query_category,
      limit=1)
    resp = requests.get(url=url, params=params)
    data = json.loads(resp.text)
    return data

f = open('/Users/tatsu/Python/K417_Project/venue_name_and_location.txt', 'w')
for i in range(len(sorted_by_user2)):
    f.write(get_venue_info(sorted_by_user2.iloc[i]['venueId'], 20130408, sorted_by_user2.iloc[i]['latitude'], sorted_by_user2.iloc[i]['longitude'], 'location')['response']['venue']['name'] + ' ' + get_venue_info(sorted_by_user2.iloc[i]['venueId'], 20130408, sorted_by_user2.iloc[i]['latitude'], sorted_by_user2.iloc[i]['longitude'], 'location')['response']['venue']['location']['formattedAddress'][0].split('-')[0] + '\n')
    time.sleep(1)

get_venue_info(sorted_by_user2.iloc[i]['venueId'], 20130408, sorted_by_user2.iloc[i]['latitude'], sorted_by_user2.iloc[i]['longitude'], 'location')['response']['venue']['location']['formattedAddress'][0].split('-')[0]

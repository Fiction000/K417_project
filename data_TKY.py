import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import time
import json, requests

visit_data_tky = pd.read_csv('foursquare-nyc-and-tokyo-check-ins/dataset_TSMC2014_TKY.csv', nrows=227429)
visit_data_nyc = pd.read_csv('foursquare-nyc-and-tokyo-check-ins/dataset_TSMC2014_NYC.csv', nrows=227429)

len(visit_data_tky)
len(visit_data_nyc)

sorted_by_user = visit_data.sort_values(by=['userId', 'utcTimestamp'])

sorted_by_user['utcTimestamp'] = pd.to_datetime(sorted_by_user['utcTimestamp'], infer_datetime_format=True)
sorted_by_user2 = sorted_by_user.sort_values(by=['userId', 'utcTimestamp'])
sorted_by_user2['utcTimestamp'] = sorted_by_user['utcTimestamp'].dt.tz_convert('Asia/Tokyo')

sorted_by_user['utcTimestamp'] = sorted_by_user['utcTimestamp'].apply(lambda s: datetime.datetime.strptime(s,'%a %b %d %H:%M:%S %z %Y'))

sorted_by_user['utcTimestamp'] = pd.to_datetime(sorted_by_user['utcTimestamp'], format='%a %b %d %H:%M:%S %z %Y')

def activity_rank(data):
    counts = []
    for i in range(len(data)):
        userId = data.iloc[i]['userId']
        counts.append(data[data['userId'] == userId].count()[0])
    counts = pd.Series(counts, name='activityCount')

    data.index = range(0, len(data))

    result = pd.concat([data, counts], axis=1)

    result = result.sort_values('activityCount', ascending=False)
    return result


activity_rank = pd.read_csv('activity_rank_UTC2.csv')

subset = activity_rank[:50010]

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

def get_venue_location(data):
    for i in range(len(data)):
        try:
            location = get_venue_info(data.iloc[i]['venueId'], 20130408, data.iloc[i]['latitude'], data.iloc[i]['longitude'], 'location')['response']['venue']['location']['formattedAddress'][0].split('-')[0]

            location_without_number = ''.join([i for i in location if not i.isdigit()])

            print(str(data['userId'][i]) + ',' + get_venue_info(data.iloc[i]['venueId'], 20130408, data.iloc[i]['latitude'], data.iloc[i]['longitude'], 'location')['response']['venue']['name'] + ',' + location_without_number + ',' + str(data['utcTimestamp'][i]))
        except KeyError:
            continue

get_venue_location()

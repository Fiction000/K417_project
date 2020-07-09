import pandas as pd
import datetime
import matplotlib.pyplot as plt
import time
import json, requests
import folium
from folium import plugins

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
    result = []
    for i in range(len(data)):
        time.sleep(0.1)
        try:
            location = get_venue_info(data.iloc[i]['venueId'], 20140408, data.iloc[i]['latitude'], data.iloc[i]['longitude'], 'location')['response']['venue']['location']['formattedAddress'][0].split('-')[0]

            location_without_number = ''.join([i for i in location if not i.isdigit()])

            result.append(str(data['userId'][i]) + ',' + get_venue_info(data.iloc[i]['venueId'], 20140408, data.iloc[i]['latitude'], data.iloc[i]['longitude'], 'location')['response']['venue']['name'] + ',' + location_without_number + ',' + str(data['utcTimestamp'][i]))

            if len(result) % 10 == 0:
                print(result[-10:])
        except KeyError:
            print('KeyError')
            continue
    print('finished!')
    return result

def get_map_with_venue_names(lat_lot, venue_name, time, userId):
    m = folium.Map(location=[40.7264, -74.005], zoom_start=12)
    tooltip = 'Click me!'
    index = 0
    try:
        for place in lat_lot:
            popup = venue_name[index] + time[index]
            folium.Marker(place, popup=popup).add_to(m)
            index += 1
    except IndexError:
        print('error occured, go on')
    m.save('marker_map_' + userId + '.html')

def activity_rank(data):
    counts = []
    for i in range(len(data)):
        userId = data.iloc[i]['userId']
        counts.append(data[data['userId'] == userId].count()[0])
    counts = pd.Series(counts, name='activityCount')

    data.index = range(0, len(data))

    result = pd.concat([data, counts], axis=1)

    result = result.sort_values('activityCount')
    return result

user_293
data_tky = pd.read_csv('activity_rank.csv')
data_nyc = pd.read_csv('foursquare-nyc-and-tokyo-check-ins/dataset_TSMC2014_NYC.csv')
active_users_tky = pd.read_csv('most_active_users2.csv')
active_users_tky.head()
active_users_tky['userId']

activity_rank_nyc = activity_rank(data_nyc)
activity_rank_nyc = activity_rank_nyc.sort_values('activityCount', ascending=False)
activity_rank_nyc.to_csv('activity_rank_nyc.csv')
activity_rank_nyc['userId'].unique()[:10]

user_293 = activity_rank_nyc[activity_rank_nyc['userId'] == 293]
user_185 = activity_rank_nyc[activity_rank_nyc['userId'] == 185]
user_354 = activity_rank_nyc[activity_rank_nyc['userId'] == 354]
user_315 = activity_rank_nyc[activity_rank_nyc['userId'] == 315]


data_tky.index = pd.to_datetime(data_tky['utcTimestamp'])
user_207 = active_users_tky[active_users_tky['userId'] == 207]
user_822 = active_users_tky[active_users_tky['userId'] == 822]
user_1541 = active_users_tky[active_users_tky['userId'] == 1541]
user_849 = active_users_tky[active_users_tky['userId'] == 849]

lat_lot = [(i,j) for i,j in zip(activity_rank_nyc[activity_rank_nyc['userId'] == 315]['latitude'], activity_rank_nyc[activity_rank_nyc['userId'] == 315]['longitude'])]
len(lat_lot)
len(user_849)

# Create a heatmap with the data.
heatmap_map = folium.Map(location=[35.575721, 139.659474], zoom_start=12)
heatmap_map.add_child(plugins.HeatMap(lat_lot))
heatmap_map.save("heatmap.html")
user_849['venueName']


venue_name = user_315[:100]['venueCategory'].tolist()
user_time = user_315['utcTimestamp'].tolist()

get_map_with_venue_names(lat_lot[:50], venue_name[:50], user_time[:50], '315')

get_venue_info(user_293.iloc[3]['venueId'], 20140408, user_293.iloc[3]['latitude'], user_293.iloc[3]['longitude'], 'location')['response']['venue']['location']['formattedAddress'][0].split('-')[0]

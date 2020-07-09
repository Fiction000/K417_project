import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import time
import json, requests
from pymining import itemmining, assocrules, perftesting
from pymining import seqmining
from pymining import itemmining

active_users = pd.read_csv('activity_rank.csv')
visit_data_NYC = pd.read_csv('~/Python/K417_Project/foursquare-nyc-and-tokyo-check-ins/dataset_TSMC2014_NYC.csv', nrows=227429)

len(active_users)

len(active_users)
len(visit_data_NYC['userId'].unique())

active_users.index = pd.to_datetime(active_users['utcTimestamp'])
visit_data_NYC.index = pd.to_datetime(visit_data_NYC['utcTimestamp'])

user_207 = active_users[active_users['userId'] == 207]
user_849 = active_users[active_users['userId'] == 849]
user_207.index = pd.DatetimeIndex(pd.to_datetime(user_207['utcTimestamp']))

venue_counts_tky = active_users['2012']['venueCategory'].value_counts()
venue_counts_nyc = visit_data_NYC['2012']['venueCategory'].value_counts()

venue_counts_tky = venue_counts_tky.sort_values()
venue_counts_nyc = venue_counts_nyc.sort_values()

# fig, ax = plt.subplots()
# fig = ax.get_figure()
# ax = venue_counts_tky.ix[-50:].plot(kind='barh', figsize=(100, 30), title='Number of Foursquare User Visitings to Places in Tokyo', fontsize=13, logx=True)
# fig.savefig('user_visitings_tokyo.png')
#
# venue_counts_nyc
# fig, ax = plt.subplots()
# fig = ax.get_figure()
# ax = venue_counts_nyc[-50:].plot(kind='barh', figsize=(100, 30), title='Number of Foursquare User Visitings to Places in NYC', fontsize=13)
# fig.savefig('user_visitings_nyc.png')
#
# df3 = pd.DataFrame({'NYC': venue_counts_nyc, 'Tokyo': venue_counts_tky})
#
# fig, ax = plt.subplots()
# fig = ax.get_figure()
# ax = df3.sort_values(by=['NYC', 'Tokyo'])[200:].plot(kind='barh', figsize=(100, 30), title='Number of Foursquare User Visitings to Places in Tokyo and NY', legend=['NY', 'Tokyo'])
# fig.savefig('user_visitings_tokyo_nyc2.png')

def plot_and_save_barh_stocked(data, plot_type, fig_title):
    customcmap = [(x/2.0,  x/4.0, 0.05) for x in range(len(data))]
    fig, ax = plt.subplots()
    ax = data.plot(kind=plot_type, figsize=(100, 30), title=fig_title, stacked=True, color=customcmap)
    fig = ax.get_figure()
    fig.savefig(fig_title)

fig, ax = plt.subplots()
fig = ax.get_figure()
ax = venue_counts_nyc.plot.bar(figsize=(100, 90), title='Number of Foursquare User Visitings to Places in NY')
fig.savefig('user_visitings_nyx.png')

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

def make_data_series(data):
    visit_counts = pd.DataFrame()
    result = []
    dates = []
    for i in range(4, 7):
        for j in range(1, 32):
            try:
                tmp = data['2012' + '-' + str(i) + '-' + str(j)]['venueCategory'].value_counts()
                if tmp.count().all() != 0:
                    result.append(tmp)
                    dates.append('2012' + '-' + str(i) + '-' + str(j))
            except KeyError:
                pass
    df = pd.concat(result, axis=1)
    return [df, dates]

user_849.index = pd.DatetimeIndex(pd.to_datetime(user_849['utcTimestamp']))

plot_and_save(df1, 'barh', 'TKY_days.png')

def make_transaction_data(data):
    result = []
    tmp = []
    df = pd.DataFrame()
    for i in range(4, 7):
        for j in range(1, 32):
            try:
                tmp = data['2012' + '-' + str(i) + '-' + str(j)][data['2012' + '-' + str(i) + '-' + str(j)] >= 1]
                if tmp.count().all() != 0:
                    result.append(tmp.index.values.tolist())
            except KeyError:
                pass
    return result

def make_user_transaction_list(data, userId):
    with open('~/Association-rule-learning/user_transaction/transaction_data_' + userId + '.dat', 'w') as f:
        for l in data:
            string = ' '.join(str(e) for e in l)
            f.write(string + '\n')

make_user_transaction_list(df2, '207')

marker_to_venue = dict(zip(df1['marker'], df1.index))
venue_to_marker = dict(zip(df1.index, df1['marker']))

def convert_marker_to_venue(marker):
    return marker_to_venue[marker]

result = []
with open('ass_rule_comb_1000.csv', 'w') as f:
    for user in active_users['userId'].unique().tolist()[:1000]:
        data = active_users[active_users['userId'] == user]
        df_user, dates = make_data_series(data)
        df_user.columns = dates
        venue_names = list(df_user.index)
        venue_names_marker = [venue_to_marker[i] for i in venue_names]

        df_user = df_user.assign(marker=pd.Series(venue_names_marker).values)
        df_user.index = df_user['marker']
        df_user = df_user.fillna(0)
        df_transactions = make_transaction_data(df_user)

        relim_input = itemmining.get_relim_input(df_transactions)
        item_sets = itemmining.relim(relim_input, min_support=2)
        rules = assocrules.mine_assoc_rules(item_sets, min_support=20, min_confidence=0.7)
        try:
            f.write("{},{},{},{}\n".format(' '.join(list(marker_to_venue[e] for e in rules[0][0])), ' '.join(list(marker_to_venue[e] for e in rules[0][1])), rules[0][2], rules[0][3]))
        except IndexError:
            continue

user_207 = active_users[active_users['userId'] == 207]
user_849 = active_users[active_users['userId'] == 849]
user_1541 = active_users[active_users['userId'] == 1541]
user_1541.index = pd.DatetimeIndex(pd.to_datetime(user_1541['utcTimestamp']))
user_207.index = pd.DatetimeIndex(pd.to_datetime(user_207['utcTimestamp']))
user_849.index = pd.DatetimeIndex(pd.to_datetime(user_849['utcTimestamp']))

df_user, dates = make_data_series(active_users)

df_user.columns = dates

venue_names = list(df_user.index)
venue_names_marker = [venue_to_marker[i] for i in venue_names]

df_user = df_user.assign(marker=pd.Series(venue_names_marker).values)

df_user.index = df_user['marker']
df_user = df_user.fillna(0)
df_user.transpose()
df_transactions = make_transaction_data(df_user)

relim_input = itemmining.get_relim_input(df_transactions)
report = itemmining.relim(relim_input, min_support=2)

item_sets = itemmining.relim(relim_input, min_support=2)
rules = assocrules.mine_assoc_rules(item_sets, min_support=20, min_confidence=0.7)
len(rules)

with open('ass_rule2.csv', 'w') as f:
    for rule in rules:
        f.write("{},{},{},{}\n".format(' '.join(list(marker_to_venue[e] for e in rule[0])), ' '.join(list(marker_to_venue[e] for e in rule[1])), rule[2], rule[3]))

rules
convert_marker_to_venue(36)

freq_seqs = seqmining.freq_seq_enum(df_transactions, 8)
len(sorted(freq_seqs))
sorted(freq_seqs)[0][0]

with open('seq_rule2.csv', 'w') as f:
    for seq in sorted(freq_seqs):
        try:
            f.write("{},{}\n".format(','.join(marker_to_venue[e] for e in seq[0]), seq[1]))
        except IndexError:
            f.write("{},{}\n".format(*seq[0], seq[1]))

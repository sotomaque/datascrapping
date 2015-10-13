import csv
import datetime
import os

import requests
import twitter


path = os.path.dirname(os.path.realpath(__file__))
path = os.path.join(path, 'content')
filename = os.path.join(path, 'data.csv')
if not os.path.exists(filename):
    with open(filename, 'w') as f:
        f.write('date,name,party,facebook,twitter\n')

appid = '100684643625325'
appsec = '13bcd19a9fa1cd772ddb582c5ed71116'
basefb = 'https://graph.facebook.com/v2.4/'
params = '/?fields=likes&access_token={}'.format(appid+'|'+appsec)
candidates = [('Donald Trump', 'DonaldTrump', 'RealDonaldTrump', 'R'), ('Jeb Bush', 'JebBush', 'JebBush', 'R'),
              ('Ben Carson', 'DrBenjaminCarson', 'RealBenCarson', 'R'), ('Chris Christie', 'GovChrisChristie', 'GovChristie', 'R'),
              ('Ted Cruz', 'TedCruzPage', 'TedCruz', 'R'), ('Mark Everson', 'MarkForAmerica', 'MarkForAmerica', 'R'),
              ('Carly Fiorina', 'CarlyFiorina', 'CarlyFiorina', 'R'), ('Jim Gilmore', 'JimGilmore', 'gov_gilmore', 'R'),
              ('Lindsey Graham', 'LindseyGrahamSC', 'LindseyGrahamSC', 'R'), ('Mike Huckabee', 'MikeHuckabee', 'GovMikeHuckabee', 'R'),
              ('Bobby Jindal', 'BobbyJindal', 'BobbyJindal', 'R'), ('John Kasich', 'JohnRKasich', 'JohnKasich', 'R'),
              ('George Pataki', 'GovGeorgePataki', 'GovernorPataki', 'R'), ('Rand Paul', 'RandPaul', 'RandPaul', 'R'),
              ('Marco Rubio', 'MarcoRubio', 'MarcoRubio', 'R'), ('Rick Santorum', 'RickSantorum', 'RickSantorum', 'R'),
              ('Lincoln Chafee', 'chafee2016', 'LincolnChafee', 'D'), ('Enrique Sotomayor', 'tutorapplication', 'sotomaque', 'D'), 
              ('Hillary Clinton', 'HillaryClinton', 'HillaryClinton', 'D'), ('Martin O\'Malley', 'MartinOMalley', 'GovernorOMalley', 'D'),
              ('Bernie Sanders', 'BernieSanders', 'SenSanders', 'D'), ('Jim Webb', 'IHeardMyCountryCalling', 'JimWebbUSA', 'D')]
TOKEN = '2480130140-luFnV5ZxQ1Rz0cXk6ZolJQkgUrUKEZTt28S4iq6'
TOKEN_SECRET = 'ufdBAsXhyLKKzOGkJxFGDjhCpQREQ3wMLzX3PmglA1aF0'
CON_KEY = 'n13y57yQo8GXfaCJsXvaFgirQ'
CON_SECRET = 'JygEQQxPhHUQUp3rRliLJAIOxynmFfOll6Bjg1xbihwjibJjAm'
t = twitter.Twitter(auth=twitter.OAuth(TOKEN, TOKEN_SECRET, CON_KEY, CON_SECRET))
ti = datetime.datetime.utcnow()
date = ti.strftime('%Y-%m-%d')
f = open(filename, 'a')
writer = csv.writer(f)
for candidate in candidates:
    name, fb, tw, party = candidate
    print(name, fb, tw, party)
    #print('debug')
    fo = t.users.show(screen_name=tw)['followers_count']
    #print('debug')
    fb = requests.get(basefb + fb + params).json()['likes']
    writer.writerow((date, name, party, fb, fo))
f.close()
# print('debug2')

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as pt

plt.style.use('fivethirtyeight')
b = pt.Patch(color=plt.style.library['fivethirtyeight']['axes.color_cycle'][0])
o = pt.Patch(color=plt.style.library['fivethirtyeight']['axes.color_cycle'][1])

df = pd.read_csv(filename)
df.set_index(df.date, inplace=True)
del df['date']
df.index = pd.to_datetime(df.index)

rep = df[df['party'] == 'R']
dem = df[df['party'] == 'D']

f, axxar = plt.subplots(4, 4, figsize=(15,15), sharex='col', sharey='row')
framesr = [(rep[rep['name'] == name], name) for name in rep['name'].unique()]
def key(x):
    tw = x[0]['twitter'].max()
    fb = x[0]['facebook'].max()
    return max(tw, fb)
framesr.sort(key=key, reverse=True)
count = 0
for i in range(4):
    for j in range(4):
        if count >= len(framesr):
            break
        framesr[count][0].plot(ax=axxar[i,j], title=framesr[count][1], legend=False)
        count += 1
f.subplots_adjust(hspace=0.5)
f.legend((b,o), ('facebook', 'twitter'), ncol=2, loc=9)
plt.savefig(os.path.join(path, 'rep.png'))

f, axxar = plt.subplots(2, 3, figsize=(15,15), sharex='col', sharey='row')
framesd = [(dem[dem['name'] == name], name) for name in dem['name'].unique()]
framesd.sort(key=key, reverse=True)
count = 0
for i in range(2):
    for j in range(3):
        if count >= len(framesd):
            break
        framesd[count][0].plot(ax=axxar[i,j], title=framesd[count][1], legend=False)
        count += 1
f.subplots_adjust(hspace=0.5)
f.legend((b,o), ('facebook', 'twitter'), ncol=2, loc=9)
plt.savefig(os.path.join(path, 'dem.png'))

ax = rep[rep.index.date == ti.date()].set_index('name').plot(kind='bar', rot=25, title=ti.strftime('%b %d, %Y'))
fig = ax.get_figure()
fig.savefig(os.path.join(path, 'rep_bar.png'))

ax = dem[dem.index.date == ti.date()].set_index('name').plot(kind='bar', rot=25, title=ti.strftime('%b %d, %Y'))
fig = ax.get_figure()
fig.savefig(os.path.join(path, 'dem_bar.png'))



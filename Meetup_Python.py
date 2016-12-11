# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
import matplotlib.pylab as mlt
import json
import urllib.request as ur
from geopy.geocoders import Nominatim

geolocator = Nominatim()

places = ["san francisco","hawai", "san diego","delhi"]
urls = []
radius = 10.0
data_format = "json"
topic = "Python"
sig_id = "208630084"
sig = "01b5445063f2d3f74a2e001556727af813ab4c62"

for place in places:
    location = geolocator.geocode(place)
    urls.append("https://api.meetup.com/2/groups?offset=0&format="+data_format+
    "&lon=" + str(location.longitude) + 
    "&topic="+ topic + 
    "&photo-host=public&page=500&radius=" + str(radius) +
    "&fields=&lat=" + str(location.latitude) + 
    "&order=id&desc=false&sig_id=" + sig_id + 
    "&sig=" +sig)
    
city,country,rating,name,members = [],[],[],[],[]
a=[]
for url in urls:
    response = ur.urlopen(url).read()
    data = json.loads(response.decode('utf-8'))
    data = data["results"] 
    a.append(data)

for i in a:
    for j in i:
        city.append(j['city'])
        country.append(j['country'])
        rating.append(j['rating'])
        name.append(j['name'])
        members.append(j['members'])

df = pd.DataFrame([city,country,rating,name,members]).T
df.columns = ['city','country','rating','name','members']
df.sort(['members','rating'])

freq = df.groupby('city').city.count()
fig = mlt.figure(figsize = (8,4))
ax = fig.add_subplot(121)
ax.set_xlabel('City')
ax.set_ylabel('Count of Groups')
ax.set_title('Number of python meetup groups')
freq.plot(kind = 'bar')

freq1 = df.groupby('city').members.sum()/df.groupby('city').members.count()
fig1 = mlt.figure(figsize = (8,4))
ax1 = fig1.add_subplot(121)
ax1.set_xlabel('City')
ax1.set_ylabel('Average Members in each group')
ax1.set_title("Python Meetup Groups")
freq1.plot(kind='bar')

freq2 = df.groupby('country').rating.sum()/df.groupby('country').rating.count()
fig2 = mlt.figure(figsize = (8,4))
ax2 = fig2.add_subplot(121)
ax2.set_xlabel('Country')
ax2.set_ylabel('Average rating')
ax2.set_title("Python Meetup Groups")
freq2.plot(kind='bar')


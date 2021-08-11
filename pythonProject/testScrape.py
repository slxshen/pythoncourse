import requests
import pandas as pd
from bs4 import BeautifulSoup

# DL and save HTML file of The Layoff Nike page 1
r = requests.get("https://www.thelayoff.com/nike")

with open("../data/thelayoff/test.html", 'w') as fd:
        fd.write(r.text)

# Put it in BeautifulSoup
soup = BeautifulSoup(r.text, 'html.parser')

# Get all time tags
all_time = soup.find_all('time')

# Create empty list
x = []

# For each time tag, extract the date and append to empty list
for i in all_time:
        if i.has_attr('data-original-title'):
                x.append(i['data-original-title'])

# Convert list to dataframe
x = pd.DataFrame(x, columns = ["time"])

# Extract date
x['dates'] = pd.to_datetime(x['time']).dt.date
#dates = pd.to_datetime(x[0]).dt.date
print(x.head())

# Plot number of posts per day
print(x['dates'].value_counts())

print(x.groupby("dates").size())
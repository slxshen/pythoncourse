import json

import requests
import pandas as pd

r = requests.get("https://careers.mcdonalds.com/api/jobs?page=2")
data = r.json()

print(r)
print(data)

print(type(data))

print(data['jobs'])
import pandas as pd

# Import
dfOrders = pd.read_csv("../data/JD_order_data.csv")

dfClicks = pd.read_csv("../data/JD_click_data.csv", iterator=True)
print(dfClicks.get_chunk(10))

# Merge click times on to order times
create table counts as
select count = count(post_id)
from posts
by category
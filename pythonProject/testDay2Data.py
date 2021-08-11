import pandas as pd

# Import
dfOrders = pd.read_csv("../data/JD_order_data.csv")
dfDelivery = pd.read_csv("../data/JD_delivery_data.csv")
dfUsers = pd.read_csv("../data/JD_user_data.csv")

# Unique # Order IDs
print(len(set(dfOrders['order_ID'])))
print(len(set(dfDelivery['order_ID'])))
print(len(set(dfOrders['user_ID'])))
print(len(set(dfUsers['user_ID'])))

# Merge orders with users
orders_users = dfOrders.merge(dfUsers, how = "outer", on = "user_ID", indicator=True)

# Merge orders with delivery
orders_delivery = dfOrders.merge(dfDelivery, on = "order_ID")

# Merge on user city
orders_delivery = orders_delivery.merge(dfUsers[['user_ID', 'city_level']], on = "user_ID")

# Are there any missing users
# No users in order file that are not in user file
# There are users in the user file that aren't in the order file
print(set(orders_users['_merge']))

# Calculate avg packages / order
print(f"Avg packages per order: {orders_delivery.groupby('order_ID')['package_ID'].count().mean()}")

# Calculate avg ship time per city
# Firsts convert date vars to date format, then get difference in hours
orders_delivery['ship'] = pd.to_datetime(orders_delivery['ship_out_time'])
orders_delivery['arr'] = pd.to_datetime(orders_delivery['arr_time'])

orders_delivery['time'] = (orders_delivery['arr'] - orders_delivery['ship']).astype('timedelta64[h]')

print(f"Avg ship time: {orders_delivery.groupby('city_level')['time'].mean().mean()}")

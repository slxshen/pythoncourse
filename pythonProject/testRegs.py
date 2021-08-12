import requests
import pandas as pd
import statsmodels as sm
import statsmodels.formula.api as smf

# Import
dfOrders = pd.read_csv("../data/JD_order_data.csv")
dfDelivery = pd.read_csv("../data/JD_delivery_data.csv")

print(f"Rows in orders: {len(dfOrders)}")
print(f"Rows in delivery: {len(dfDelivery)}")

# Roll delivery up to order level
order_del_times = dfDelivery.groupby('order_ID')['ship_out_time', 'arr_time'].max()
print(order_del_times.head())
print(order_del_times.describe())

# Merge orders and delivery together, while limiting to promise = 1
orders_delivery = dfOrders[(dfOrders['promise'] == "0") | (dfOrders['promise'] == "1")][['order_ID', 'order_date', 'order_time']].merge(order_del_times, on = "order_ID", indicator = True, how = 'inner')
print(f"Rows in merge: {len(orders_delivery)}")

print(orders_delivery.head())
for col in orders_delivery.columns:
    print(col)

# Convert ship date vars to date format, then get delivery time in hours
orders_delivery['ship'] = pd.to_datetime(orders_delivery['ship_out_time'])
orders_delivery['arr'] = pd.to_datetime(orders_delivery['arr_time'])

# Get hour of order time
orders_delivery['order_time'] = pd.to_datetime(orders_delivery['order_time']).dt.time
orders_delivery['order_time_hrs'] = orders_delivery['order_time'].astype(str).str.split(':', 1, expand = True)[0].astype(int)

# Calculate delivery time
orders_delivery['time_to_del'] = (orders_delivery['arr'] - orders_delivery['ship']).astype('timedelta64[h]')
print(orders_delivery.head())
print(orders_delivery.describe())

# Filter 0 < delivery time < 72 hours
orders_delivery = orders_delivery[(orders_delivery['time_to_del'] > 0) & (orders_delivery['time_to_del'] <= 72)]
print(f"Remaining rows: {len(orders_delivery)}")

# Reg delivery time on order time
results = smf.ols('time_to_del ~ order_time_hrs', data = orders_delivery).fit()
print(results.summary())
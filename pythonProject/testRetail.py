import pandas as pd

# df = pd.read_csv("../data/JD_order_data.csv")
# df.to_parquet("../data/JD_order_data.parquet")
df = pd.read_parquet("../data/JD_order_data.parquet")

print(df.head())

# Avg number SKUs purchased per user
SkusByUser = df.groupby(by = "user_ID")['quantity'].count()
print(f"Avg SKUs per user: {SkusByUser.mean()}")

# solution
mean_purchases = df.groupby('user_ID').size().mean()
print(f"(Solution) Mean SKUs purchased per user: {mean_purchases}")

# Most expensive order placed
df['cost'] = df['final_unit_price'] * df['quantity']
# Orders = df.groupby(by = "order_ID")['cost'].sum()
# print(Orders.head())

Orders = df.groupby(by = ["order_ID", "user_ID"])['cost'].sum()
print(Orders.head())
print(f"Most exp order and user ID: {Orders.idxmax(axis = 1)}")
print(f"Most exp order cost: {Orders.max()}")

# solution
orders = df.groupby('order_ID')['cost'].sum()
most_exp = df[df['order_ID'] == orders.idxmax(axis = 1)]
print(f"(Solution) Most exp order: \n {most_exp.to_string()}")

# Largest number of orders placed by a singer user
largest = Orders.groupby(by= "user_ID").count().max()
print(f"Largest number of orders: {largest}")

# solution
max_purchases = df.groupby('user_ID').agg({'order_ID': 'nunique'})['order_ID'].max()
print(f"(Solution) Most orders placed by a user: {max_purchases}")
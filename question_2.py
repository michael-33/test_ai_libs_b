import pandas as pd
import matplotlib.pyplot as plt

items_df = pd.read_csv('src/data/Items.csv')
customers_df = pd.read_csv('src/data/customers.csv')
orders_df = pd.read_csv('src/data/orders.csv')
order_item_df = pd.read_csv('src/data/order_item.csv')

## section 1

# 2
customer_purchases = order_item_df.merge(
    orders_df[['order_id', 'customer_id']],
    on='order_id',
    how='left'
).groupby('customer_id')['quantity'].sum().sort_values(ascending=False)
print(customer_purchases.head(1))

# 3
purchases_with_prices = order_item_df.merge(
    items_df[['id', 'item_price']],
    left_on='item_id',
    right_on='id',
    how='left'
).rename(columns={'id_x': 'id'}).drop('id_y', axis=1)
purchases_with_prices['total_price'] = purchases_with_prices['item_price'] * purchases_with_prices['quantity']

# 4
print("purchases_with_prices")
print(purchases_with_prices)

# 5
max_purchase = purchases_with_prices['total_price'].max()
min_purchase = purchases_with_prices['total_price'].min()
avg_purchase = purchases_with_prices['total_price'].mean()

print(max_purchase)
print(min_purchase)
print(avg_purchase)

# 6
pivot_table = pd.pivot_table(
    customers_df,
    values='id',
    index='nationallity',
    columns='gender',
    aggfunc='count',
    fill_value=0
)
print(pivot_table)

## section 2

# 4
customers_df['joining_year'] = pd.to_datetime(customers_df['joining_date'], format='%d/%m/%Y').dt.year
customers_by_year = customers_df.groupby('joining_year').size()

bars = plt.bar(customers_by_year.index, customers_by_year.values)
plt.title('New customers by year')
plt.xlabel('Year')
plt.ylabel('Amount')
plt.bar_label(bars)
plt.show()



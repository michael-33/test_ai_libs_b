import pandas as pd

items_df = pd.read_csv('src/data/Items.csv')
customers_df = pd.read_csv('src/data/customers.csv')
orders_df = pd.read_csv('src/data/orders.csv')
order_item_df = pd.read_csv('src/data/order_item.csv')

# # data exploration
print(items_df.info())
print(customers_df.info())
print(orders_df.info())
print(order_item_df.info())

print(items_df.describe(include='all'))
print(customers_df.describe(include='all'))
print(orders_df.describe(include='all'))
print(order_item_df.describe(include='all'))

print(items_df.head())
print(customers_df.head())
print(orders_df.head())
print(order_item_df.head())

# dupication deletion
items_df['amount_of_not_null_values'] = items_df.notna().sum(axis=1)
sorted_items_df = items_df.sort_values(by=['amount_of_not_null_values'], ascending=False)
items_df_without_duplicates = sorted_items_df.drop_duplicates(subset=['item_name'], keep='first')
# print(items_df_without_duplicates)

# update order_item table
id_mapping = items_df.merge(
    items_df_without_duplicates[['id', 'item_name']],
    on='item_name',
    how='left'
).set_index('id_x')['id_y']

order_item_df['item_id'] = order_item_df['item_id'].map(id_mapping)
print(order_item_df)

# delete customers with fewer than 3 orders
customer_order_count = orders_df['customer_id'].value_counts()
customers_to_keep = customer_order_count[customer_order_count >= 3].index
customers_df = customers_df[customers_df['id'].isin(customers_to_keep)]
print(customers_df)

orders_df = orders_df[orders_df['customer_id'].isin(customers_to_keep)]
order_item_df = order_item_df[order_item_df['order_id'].isin(orders_df['order_id'])]
print(order_item_df)

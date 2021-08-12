"""Re-do the prior analysis with a SQLite database."""

import sqlite3
from pathlib import Path

import pandas as pd


def main():
    """Run all the parts of this task."""

    # delete the database file if it already exists
    db_path = Path('../../data/db.sqlite')
    db_path.unlink(missing_ok=True)

    # create the database
    with sqlite3.connect(db_path) as connection:
        create_database(connection)


def create_database(connection):
    """Create tables for orders, delivery, and clicks."""
    cursor = connection.cursor()

    # create an orders table, dropping some duplicate rows to satisfy the primary key constraint
    print("Creating orders table ...")
    cursor.execute('''
        CREATE TABLE JD_order_data (
            order_ID TEXT NOT NULL CHECK(LENGTH(order_ID) = 10),
            sku_ID TEXT NOT NULL CHECK(LENGTH(sku_ID) = 10),
            user_ID TEXT NOT NULL CHECK(LENGTH(user_ID) = 10),
            order_time DATETIME NOT NULL,
            quantity INT NOT NULL,
            final_unit_price REAL NOT NULL,
            PRIMARY KEY (order_ID, sku_ID)
        )
    ''')
    orders = pd.read_csv('../../data/JD_order_data.csv', low_memory=False)
    orders = orders[['order_ID', 'sku_ID', 'user_ID', 'order_time', 'quantity', 'final_unit_price']]
    orders = orders.groupby(['order_ID', 'sku_ID'], as_index=False).first()
    orders.to_sql('JD_order_data', connection, index=False, if_exists='append')
    cursor.execute('CREATE INDEX orders_user_index ON JD_order_data (user_ID)')

    # create a delivery table
    print("Creating delivery table ...")
    cursor.execute('''
        CREATE TABLE JD_delivery_data (
            order_ID TEXT NOT NULL CHECK(LENGTH(order_ID) = 10),
            package_ID TEXT NOT NULL CHECK(LENGTH(package_ID) = 10),
            ship_out_time DATETIME NOT NULL,
            PRIMARY KEY (order_ID, package_ID),
            FOREIGN KEY (order_ID) REFERENCES JD_order_data (order_ID)
        )
    ''')
    delivery = pd.read_csv('../../data/JD_delivery_data.csv', parse_dates=['ship_out_time'])
    delivery = delivery[['order_ID', 'package_ID', 'ship_out_time']]
    delivery.to_sql('JD_delivery_data', connection, index=False, if_exists='append')

    # create a clicks table
    print("Creating clicks table ...")
    cursor.execute('''
        CREATE TABLE JD_click_data (
            user_ID TEXT NOT NULL CHECK(LENGTH(user_ID) = 10),
            sku_ID TEXT NOT NULL CHECK(LENGTH(sku_ID) = 10),
            request_time DATETIME NOT NULL,
            FOREIGN KEY (user_ID) REFERENCES JD_order_data (user_ID),
            FOREIGN KEY (sku_ID) REFERENCES JD_order_data (sku_ID)
        )
    ''')
    clicks = pd.read_csv('../../data/JD_click_data.csv', parse_dates=['request_time'])
    clicks = clicks[clicks['user_ID'] != '-']
    clicks = clicks[['user_ID', 'sku_ID', 'request_time']]
    clicks.to_sql('JD_click_data', connection, index=False, if_exists='append')
    cursor.execute('CREATE INDEX clicks_user_index ON JD_click_data (user_ID)')
    cursor.execute('CREATE INDEX clicks_sku_index ON JD_click_data (sku_ID)')

    # Create a user table
    print("Creating users table ...")
    cursor.execute('''
            CREATE TABLE JD_user_data (
                user_ID TEXT NOT NULL CHECK(LENGTH(user_ID) = 10),
                plus INT NOT NULL CHECK (plus IN (0, 1)),
                PRIMARY KEY (user_ID)
            )
        ''')
    users = pd.read_csv('../../data/JD_user_data.csv', low_memory=False)
    users = users[['user_ID', 'plus']]
    users = users.groupby(['user_ID'], as_index=False).first()
    users.to_sql('JD_user_data', connection, index=False, if_exists='append')
    cursor.execute('CREATE INDEX users_user_index ON JD_user_data (user_ID)')



if __name__ == '__main__':
    main()

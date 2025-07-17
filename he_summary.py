import mysql.connector
from tabulate import tabulate

def fetch_all_stock_data():
    try:
        # Establish MySQL connection
        conn =  mysql.connector.connect(host="localhost", user="root", password="123", database="hitman")
        cursor = conn.cursor()
        
        # Query to fetch all stock data
        query = "SELECT * FROM stock_transactions"
        cursor.execute(query)
        
        # Fetch column names
        columns = [desc[0] for desc in cursor.description]
        
        # Fetch all rows
        result = cursor.fetchall()
        
        # Close the connection
        cursor.close()
        conn.close()
        
        return columns, result
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None, None

# Example usage
if __name__ == "__main__":
    columns, data = fetch_all_stock_data()
    if data:
        print(tabulate(data, headers=columns, tablefmt="grid"))
    else:
        print("No data found.")

#------------------------------------------------------------------------
import mysql.connector
import pandas as pd
from collections import deque
from tabulate import tabulate  

class InvestmentCalculator:
    def __init__(self, db_config):
        self.db_config = db_config
        self.transactions = {}  
        self.fetch_stock_transactions()

    def fetch_stock_transactions(self):
        """Fetch stock transactions from the database, ordered by activity_date for FIFO processing."""
        connection = mysql.connector.connect(**self.db_config)
        cursor = connection.cursor()

        query = """
        SELECT LOWER(instrument), tran_code, quantity, price, activity_date 
        FROM stock_transactions 
        ORDER BY activity_date ASC
        """
        cursor.execute(query)

        for instrument, transaction_type, qty, price, activity_date in cursor.fetchall():
            if instrument not in self.transactions:
                self.transactions[instrument] = {"buy": deque(), "sell": []}
            
            if transaction_type.lower() == 'buy':
                self.transactions[instrument]["buy"].append((qty, price, activity_date))  
            elif transaction_type.lower() == 'sell':
                self.transactions[instrument]["sell"].append((qty, price, activity_date))  

        cursor.close()
        connection.close()

    def calculate(self):
        """Calculate investment metrics using FIFO and return as a DataFrame."""
        table_data = []

        for instrument, data in self.transactions.items():
            buy_queue = data["buy"]
            total_qty = 0
            total_investment = 0

            # Process sales using FIFO
            for sell_qty, sell_price, sell_date in data["sell"]:
                while sell_qty > 0 and buy_queue:
                    buy_qty, buy_price, buy_date = buy_queue.popleft()
                    
                    if buy_qty <= sell_qty:
                        sell_qty -= buy_qty
                    else:
                        buy_queue.appendleft((buy_qty - sell_qty, buy_price, buy_date))
                        sell_qty = 0

            # Remaining buys contribute to current investment
            for qty, price, buy_date in buy_queue:
                total_qty += qty
                total_investment += qty * price

            avg_price = total_investment / total_qty if total_qty > 0 else 0

            table_data.append([instrument.upper(), total_investment, total_qty, avg_price])

        df = pd.DataFrame(table_data, columns=["Instrument", "Total Investment", "Total Quantity", "Average Price"])
        df["Average Price"] = df["Average Price"].fillna(0)  

        self.insert_data_into_db(df)  # Store results in MySQL

        return df

    def insert_data_into_db(self, df):
        """Insert calculated investment data into MySQL database."""
        connection = mysql.connector.connect(**self.db_config)
        cursor = connection.cursor()

        # Insert or update records in the summary table
        for _, row in df.iterrows():
        
            query = """
            INSERT INTO summary (instrument, total_investment, total_quantity, average_price) 
            VALUES (%s, %s, %s, %s) 
            ON DUPLICATE KEY UPDATE 
                total_investment = VALUES(total_investment),
                total_quantity = VALUES(total_quantity),
                average_price = VALUES(average_price)
            """
            cursor.execute(query, (row["Instrument"], row["Total Investment"], row["Total Quantity"], row["Average Price"]))

        connection.commit()
        cursor.close()
        connection.close()
        print("data stored successfully ")

# Database Configuration (Update with your credentials)
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '123',
    'database': 'hitman'
}

# Example Usage
calculator = InvestmentCalculator(db_config)
result_df = calculator.calculate()

# Display result in table format
print(tabulate(result_df, headers="keys", tablefmt="grid", showindex=False))



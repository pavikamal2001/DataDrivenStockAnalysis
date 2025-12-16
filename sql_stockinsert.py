import psycopg2
import pandas as pd

# -------------------------------------
# CONNECT TO SQL DATABASE
# -------------------------------------
connection = psycopg2.connect(
    host="localhost",
    database="stockdb",
    user="postgres",
    password="Pavikamal29",
    port="5432"
)

cursor = connection.cursor()
print("Connected to PostgreSQL!")


# -------------------------------------
# FUNCTION TO INSERT CSV INTO TABLE
# -------------------------------------
def insert_csv(csv_path, table_name):
    df = pd.read_csv(csv_path)
    if table_name == "stock_correlation_matrix":
        # Replace dashes, ampersands, spaces with underscores
        df.columns = [c.replace("-", "_").replace("&", "_").replace(" ", "_") for c in df.columns]
    columns = ",".join(df.columns)
    
    for _, row in df.iterrows():
        placeholders = ",".join(["%s"] * len(row))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        cursor.execute(query, tuple(row))

    connection.commit()
    print(f"{len(df)} rows inserted into {table_name}")


    


# -------------------------------------
# INSERT ALL 5 CSV FILES
# -------------------------------------

insert_csv(r"C:\Users\Admin\OneDrive\Desktop\Project_2\top10_volatile_stocks.csv", 
           "top10_volatile_stocks")

insert_csv(r"C:\Users\Admin\OneDrive\Desktop\Project_2\top5_cumulative_return.csv", 
           "top5_cumulative_return")

insert_csv(r"C:\Users\Admin\OneDrive\Desktop\Project_2\sector_performance.csv",
           "sector_performance")

insert_csv(r"C:\Users\Admin\OneDrive\Desktop\Project_2\stock_correlation_matrix.csv", 
           "stock_correlation_matrix")

insert_csv(r"C:\Users\Admin\OneDrive\Desktop\Project_2\top5_gainers_losers_allMonths.csv", 
           "top5_gainers_losers_allmonths")


insert_csv(r"C:\Users\Admin\OneDrive\Desktop\Project_2\top10_green_stocks.csv",
           "top10_green_stocks")



insert_csv(r"C:\Users\Admin\OneDrive\Desktop\Project_2\top10_loss_stocks.csv",
           "top10_loss_stocks")

insert_csv(r"C:\Users\Admin\OneDrive\Desktop\Project_2\market_summary.csv",
           "market_summary")





print("All CSVs inserted successfully!")

cursor.close()
connection.close()

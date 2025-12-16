import yaml
import pandas as pd
import os

folder_path = r"C:/Users/Admin/OneDrive/Desktop/Project_2/Data Folder"

all_records = []

#  Read ALL YAML files from all subfolders ─── #
for root, dirs, files in os.walk(folder_path):
    for file in files:
        if file.endswith((".yaml", ".yml")):
            full_path = os.path.join(root, file)

            with open(full_path, "r") as f:
                day_data = yaml.safe_load(f)

                # YAML file contains list of 50 ticker dictionaries
                if isinstance(day_data, list):
                    for rec in day_data:
                        all_records.append(rec)

# ─── Step 2: DataFrame
df = pd.DataFrame(all_records)

#  columns exist
df = df[['Ticker', 'close', 'date']]

#  Create Output Folder ─── #
output_path = r"C:/Users/Admin/OneDrive/Desktop/Project_2/Output_CSV"
os.makedirs(output_path, exist_ok=True)

#  Split into 50 CSV files ─── #
for ticker, ticker_df in df.groupby('Ticker'):
    file_name = f"{output_path}/{ticker}.csv"
    ticker_df.to_csv(file_name, index=False)

print("✓ CSV files created successfully!")


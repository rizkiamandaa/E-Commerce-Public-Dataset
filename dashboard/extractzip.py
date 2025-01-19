import zipfile
import pandas as pd
import io

# Path file ZIP
zip_file_path = "all_df.zip"

# Membuka file ZIP dan membaca file CSV langsung dari memori
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    # Menentukan nama file CSV dalam ZIP
    csv_file_name = 'all_df.csv'  # Ganti dengan nama file CSV yang ada di dalam ZIP
    with zip_ref.open(csv_file_name) as csv_file:
        all_df = pd.read_csv(csv_file)

all_df.head()
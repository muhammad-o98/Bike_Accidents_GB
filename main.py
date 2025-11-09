# main.py
from src.etl import merge_accidents_bikers
from src.preprocessing import preprocess, save_parquet
from src.eda import accidents_over_time, severity_distribution, accidents_by_gender_age
import os

# Paths
accidents_path = "data/Accidents.csv"
bikers_path = "data/Bikers.csv"
parquet_path = "processed/bicycle_accidents.parquet"


# ETL
print("Merging datasets...")
df = merge_accidents_bikers(accidents_path, bikers_path)
print(f"Combined dataset shape: {df.shape}")

# Preprocessing
print("Preprocessing data...")
df_clean = preprocess(df)
print("Preprocessing complete.")

# Save processed Parquet
print(f"Saving processed dataset to {parquet_path} ...")
save_parquet(df_clean, parquet_path)
print("Parquet file saved.")


# Generate and save plots
print("Generating EDA plots...")
accidents_over_time(df_clean)
severity_distribution(df_clean)
accidents_by_gender_age(df_clean)
print("All plots saved to processed/ folder.")

# ---------------------------
# Done
# ---------------------------
print("Pipeline complete. Dataset and plots are ready.")

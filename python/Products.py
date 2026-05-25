import pandas as pd
import os

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Construct the path to the products dataset
file_path = os.path.join(script_dir, "..", "data", "products.csv")

# Load products dataset
df = pd.read_csv(file_path)

# Print unique categories
print("Product Categories:")
print(df["category"].unique())

# Count categories
print("\nCategory Counts:")
print(df["category"].value_counts())
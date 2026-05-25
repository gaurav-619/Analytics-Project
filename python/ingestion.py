from pytrends.request import TrendReq
import pandas as pd

# Initialize pytrends
pytrends = TrendReq()

# Your categories
keywords = [
    "Grocery",
    "Fashion",
    "Electronics",
    "Sports",
    "Beauty"
]

# Fetch trends
pytrends.build_payload(keywords, timeframe='today 12-m')

data = pytrends.interest_over_time()

# Remove isPartial column
data = data.drop(columns=['isPartial'])

import os
# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Construct the path to the google_trends.csv file
file_path = os.path.join(script_dir, "..", "data", "google_trends.csv")

# Save to CSV
data.to_csv(file_path)

print("Google Trends data saved successfully")
print(data.head())
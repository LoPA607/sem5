import requests
import json
from datetime import datetime

lat, lon = 28.6139, 77.2090

url = (
    "https://power.larc.nasa.gov/api/temporal/daily?"
    f"parameters=T2M,T2M_MAX,T2M_MIN,RH2M,PRECTOT,WS10M,ALLSKY_SFC_SW_DWN"
    f"&community=AG"
    f"&longitude={lon}"
    f"&latitude={lat}"
    f"&start=20100101"
    f"&end=20151231"
    f"&format=JSON"
)

print("Fetching weather data...")
response = requests.get(url).json()
daily_data = response["properties"]["parameter"]

# Convert to list of dictionaries for easier viewing
data_list = []
for date, values in sorted(daily_data.items()):
    row = {'date': date}
    row.update(values)
    data_list.append(row)

# Show first 5 records
print(f"\nFound {len(data_list)} daily records from 2010-2015")
print("\nFirst 5 records:")
for i, record in enumerate(data_list[:5]):
    print(f"\n{i+1}. Date: {record['date']}")
    for param, value in record.items():
        if param != 'date':
            print(f"   {param}: {value}")

print(f"\nParameters available:")
if data_list:
    params = [k for k in data_list[0].keys() if k != 'date']
    for param in params:
        print(f"- {param}")

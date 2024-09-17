import requests
import random
from datetime import datetime, timedelta
import faker
from faker import Faker
import mysql.connector
import requests
import random

#####residential and business address api
def fetch_all_records(api_url, limit, offset=0):
    params = {'limit': limit, 'offset': offset}
    response = requests.get(api_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        records = data.get('result', {}).get('records', [])
        return records
    else:
        print("Error:", response.status_code)
        return []

def get_random_record(records, address_column_name):
    if records:
        random_record = random.choice(records)
        lat = float(random_record.get('latitude', 0))
        long = float(random_record.get('longitude', 0))
        address = random_record.get(address_column_name, 'Unknown address')
        return lat, long, address
    else:
        print("No records available.")
        return None

# Example usage
vic_residential_api_url = 'https://discover.data.vic.gov.au/api/3/action/datastore_search?resource_id=6ec3d5b8-5a3c-48b9-9256-f46ef578eaa1'
vic_business_api_url = 'https://discover.data.vic.gov.au/api/3/action/datastore_search?resource_id=5a781178-9508-4628-ba9c-dc72a156ef99'

residential_records = []
limit = 32000
offset = 0
while True:
    records = fetch_all_records(vic_residential_api_url, limit, offset)
    if not records:
        break
    residential_records.extend(records)
    offset += limit

business_records = []
limit = 32000
offset = 0
while True:
    records = fetch_all_records(vic_business_api_url, limit, offset)
    if not records:
        break
    business_records.extend(records)
    offset += limit

print(len(residential_records))
print(len(business_records))

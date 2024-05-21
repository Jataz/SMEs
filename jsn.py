import pandas as pd
import json
import os

def create_django_fixture_from_excel(excel_file_path, json_file_path):
    # Read the Excel file
    df = pd.read_excel(excel_file_path)

    provinces = {}
    districts = {}
    wards = []

    province_id_counter = 1
    district_id_counter = 1
    ward_id_counter = 1

    for _, row in df.iterrows():
        province_name = row['Province']
        district_name = row['District']
        ward_name = row['Ward']

        # Add province if not already added
        if province_name not in provinces:
            provinces[province_name] = {
                "model": "smeapp.province",
                "pk": province_id_counter,
                "fields": {
                    "province_name": province_name
                }
            }
            province_id_counter += 1

        # Add district if not already added
        if district_name not in districts:
            districts[district_name] = {
                "model": "smeapp.district",
                "pk": district_id_counter,
                "fields": {
                    "district_name": district_name,
                    "province_id": provinces[province_name]['pk']
                }
            }
            district_id_counter += 1

        # Add ward
        wards.append({
            "model": "smeapp.ward",
            "pk": ward_id_counter,
            "fields": {
                "ward_name": ward_name,
                "district_id": districts[district_name]['pk']
            }
        })
        ward_id_counter += 1

    # Combine all data into a single list
    fixture_data = list(provinces.values()) + list(districts.values()) + wards

    # Convert the data to JSON and save to a file
    with open(json_file_path, 'w') as jsonfile:
        json.dump(fixture_data, jsonfile, indent=4)

# Ensure the script is not named pandas.py and check for circular imports
if __name__ == "__main__":
    excel_file_path = 'wards.xlsx'
    json_file_path = 'django_fixture.json'

    create_django_fixture_from_excel(excel_file_path, json_file_path)

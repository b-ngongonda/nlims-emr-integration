import pandas as pd
from datetime import datetime
import requests

# Define the month and day encoding map
month_day_map = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C",
                 "E", "F", "G", "H", "Y", "J", "K", "Z", "M", "N", "O", "P",
                 "Q", "R", "S", "T", "V", "W", "X"]

# Mapping of site codes
site_code_mapping = {
    "Ligowe HC": "LGWE",
    "Nsambe HC": "NSM",
    "Neno District Hospital": "NNO"
}

# Initialize counters for each health_facility_name to ensure unique tracking numbers
counters = {}

def generate_tracking_number(health_facility_name, date_sample_drawn):
    """Generate a tracking number based on health_facility_name, date, and a counter."""
    # Get the site code
    site_code = site_code_mapping.get(health_facility_name, "UNK")  # Default to "UNK" if health_facility_name not found

    # Parse the visit date
    date_sample_drawn = date_sample_drawn.replace('-', '/')  # Convert to consistent format
    date_sample_drawntime = datetime.strptime(date_sample_drawn, "%Y/%m/%d")
    year = str(date_sample_drawntime.year)[-1]  # Last digit of the year
    month = month_day_map[date_sample_drawntime.month - 1]
    day = month_day_map[date_sample_drawntime.day - 1]

    # Get or initialize the counter for this health_facility_name and date
    counter_key = (site_code, date_sample_drawn)
    if counter_key not in counters:
        counters[counter_key] = 1
    counter = counters[counter_key]

    # Construct the tracking number
    tracking_number = f"X{site_code}{year}{month}{day}{counter}"

    # Increment the counter for the next use
    counters[counter_key] += 1

    return tracking_number

# Load the dataset
data = pd.read_csv("Neno_viral_load_patients.csv")

# Drop rows with missing date_sample_drawn
data_cleaned = data.dropna(subset=['date_sample_drawn'])

# Ensure date_sample_drawn is treated as string
data_cleaned['date_sample_drawn'] = data_cleaned['date_sample_drawn'].astype(str)

# Generate tracking numbers
data_cleaned['tracking_number'] = data_cleaned.apply(
    lambda row: generate_tracking_number(row['health_facility_name'], row['date_sample_drawn']),
    axis=1
)

# Reorder columns to place tracking_number first
columns = ['tracking_number'] + [col for col in data_cleaned.columns if col != 'tracking_number']
data_cleaned = data_cleaned[columns]

# Save the updated dataset to an Excel file
output_file = "Updated_Neno_viral_load_patients.xlsx"
data_cleaned.to_excel(output_file, index=False)

print(f"Tracking numbers generated and saved to {output_file}")

# Define the API endpoint and token
api_endpoint = "http://18.219.226.28:3009/api/v1/create_order"
api_token = "zmPIbLskFXOz"
headers = {
    "token": api_token,
    "Content-Type": "application/json"
}

# Post each row as a request
def post_data(row):
    payload = {
        "tracking_number": row["tracking_number"],
        "district": row.get("district", "Unknown"),
        "health_facility_name": row.get("health_facility_name", "Unknown"),
        "first_name": row.get("first_name", "Unknown"),
        "last_name": row.get("last_name", "Unknown"),
        "phone_number": row.get("phone_number", "Unknown"),
        "gender": row.get("gender", "Unknown"),
        "arv_number": row.get("arv_number", "Unknown"),
        "art_regimen": row.get("art_regimen", "Unknown"),
        "art_start_date": row.get("art_start_date", "Unknown"),
        "date_of_birth": row.get("date_of_birth", "Unknown"),
        "national_patient_id": row.get("national_patient_id", "Unknown"),
        "requesting_clinician": row.get("requesting_clinician", "Unknown"),
        "sample_type": row.get("Plasma", "DBS"),
        "tests": ["Viral Load"],
        "date_sample_drawn": row.get("date_sample_drawn", "Unknown"),
        "sample_priority": row.get("sample_priority", "Routine"),
        "sample_status": row.get("sample_status", "specimen_collected"),
        "target_lab": row.get("target_lab", "Unknown"),
        "order_location": row.get("Lighthouse", "Unknown"),
        "who_order_test_first_name": row.get("who_order_test_first_name", "Unknown"),
        "who_order_test_last_name": row.get("who_order_test_last_name", "Unknown")
    }
    response = requests.post(api_endpoint, headers=headers, json=payload)
    return response.status_code, response.text

# Iterate over each row and make API requests
for _, row in data_cleaned.iterrows():
    status, response = post_data(row)
    print(f"Posted tracking number {row['tracking_number']}: Status {status}, Response: {response}")


# Define the API endpoint for querying results
query_endpoint = "http://18.219.226.28:3009/api/v1/query_results_by_tracking_number"

def query_results_by_tracking_number(tracking_number):
    """Query results for a specific tracking number."""
    response = requests.get(f"{query_endpoint}/{tracking_number}", headers=headers)
    if response.status_code == 200:
        result_data = response.json()
        viral_load_data = result_data.get("data", {}).get("results", {}).get("Viral Load", {})
        viral_load = viral_load_data.get("Viral Load", "Not Available")
        result_date = viral_load_data.get("result_date", "Not Available")
        return viral_load, result_date
    else:
        return "Error", "Error"

# Add Viral Load and result_date columns to the dataframe
data_cleaned["Viral Load"] = None
data_cleaned["Result Date"] = None

# Query each tracking number and append the results
for index, row in data_cleaned.iterrows():
    viral_load, result_date = query_results_by_tracking_number(row["tracking_number"])
    data_cleaned.at[index, "Viral Load"] = viral_load
    data_cleaned.at[index, "Result Date"] = result_date
    print(f"Queried tracking number {row['tracking_number']}: Viral Load={viral_load}, Result Date={result_date}")

# Save the updated dataset to a new Excel file
output_file_with_results = "Updated_Neno_viral_load_with_results.xlsx"
data_cleaned.to_excel(output_file_with_results, index=False)

print(f"Updated dataset with results saved to {output_file_with_results}")


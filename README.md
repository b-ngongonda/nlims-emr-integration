# NLIMS and EMR API Integration

This Python script automates the generation of unique tracking numbers for viral load samples collected at healthcare facilities in Neno District, Malawi. It integrates with a National laboratory information management system (NLIMS) API to create orders and query results, streamlining the tracking and management of patient viral load data.

## Features

- **Tracking Number Generation**:
  - Generates unique tracking numbers based on the health facility, date, and a counter.
  - Encodes the month and day using a predefined mapping system.
- **Data Cleaning and Validation**:
  - Cleans and validates input data to handle missing or invalid dates.
- **API Integration**:
  - Posts patient and sample data to an external NLIMS API.
  - Retrieves viral load results using generated tracking numbers.
- **Token-Based Authentication**:
  - Dynamically re-authenticates to fetch an API token, reused across the session.
- **Output Files**:
  - Generates an Excel file with tracking numbers: `Updated_Neno_viral_load_patients.xlsx`.
  - Produces an updated file with queried viral load results: `Updated_Neno_viral_load_with_results.xlsx`.

## Requirements

- Python 3.6 or higher
- Required Python libraries:
  - `pandas`
  - `requests`
  - `openpyxl`

## How It Works

1. **Input Data**:
   - Reads patient data from a CSV file (`Neno_viral_load_patients.csv`).
   - Ensures the `date_sample_drawn` column is valid and formatted correctly.

2. **Tracking Number Generation**:
   - Uses the facility name, date of sample collection, and a counter to create a unique tracking number for each sample.

3. **API Interaction**:
   - Posts sample and patient data to the LIMS API to create orders.
   - Queries the LIMS API for viral load results using the tracking numbers.

4. **Output**:
   - Saves processed data with tracking numbers in `Updated_Neno_viral_load_patients.xlsx`.
   - Updates the file with viral load results in `Updated_Neno_viral_load_with_results.xlsx`.

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo-name.git
2. cd your-repo-name:
   ```bash
   cd your-repo-nam
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
4. Ensure the input CSV file (Neno_viral_load_patients.csv) is in the correct format.
5. Run the script:
   ```bash
   python emr_nlims_integrator.py



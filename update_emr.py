import requests
from requests.auth import HTTPBasicAuth

# OpenMRS server details
base_url = "http://localhost:8081/openmrs/ws/rest/v1"
username = "bngongonda"
password = "brtxyz1000"

# Encounter and Observation Details
encounter_uuid = "0002699b-395b-4cd4-815e-ca04761beb33"  # Correct Encounter UUID
patient_uuid = "c4ed957e-2695-102d-b4c2-001d929acb54"
location_uuid = "0d414ce2-5ab4-11e0-870c-9f6107fee88e"
form_uuid = "badbb502-9718-11e7-8999-ad34fd5ac8df"
new_obs_uuid_to_void = "5c2db740-a486-441f-ac40-1abdbad812a6"  # Observation UUID to void
new_obs_concept_uuid = "69e87644-5562-11e9-8647-d663bd873d93"  # Concept UUID for new observation
new_obs_value = "40"  # New value for observation
obs_datetime = "2024-01-02T00:00:00.000+0000"  # Updated to 2020-11-26


# Function to void an existing observation
def void_observation(obs_uuid, reason="Updating observation value"):
    url = f"{base_url}/obs/{obs_uuid}"
    params = {"reason": reason}
    response = requests.delete(url, params=params, auth=HTTPBasicAuth(username, password))

    if response.status_code == 204:
        print(f"Successfully voided observation: {obs_uuid}")
    else:
        print(f"Failed to void observation: {obs_uuid}")
        print(f"Error: {response.text}")
        exit(1)


# Function to add a new observation to an existing encounter
def add_observation_to_encounter(encounter_uuid, concept_uuid, new_obs_value, obs_datetime):
    url = f"{base_url}/obs"
    payload = {
        "encounter": encounter_uuid,
        "person": patient_uuid,
        "concept": concept_uuid,
        "value": new_obs_value,
        "obsDatetime": obs_datetime  # Updated obsDatetime
    }

    response = requests.post(url, json=payload, auth=HTTPBasicAuth(username, password))

    if response.status_code in [200, 201]:
        print("Successfully added a new observation to the encounter.")
        print("Response:", response.json())
    else:
        print("Failed to add observation to the encounter.")
        print(f"Error: {response.text}")
        exit(1)


# Main process
if __name__ == "__main__":
    print("Starting observation update process...")

    # Step 1: Void the existing observation
    print("Voiding existing observation...")
    void_observation(new_obs_uuid_to_void)

    # Step 2: Add new observation to the existing encounter
    print("Adding new observation to the existing encounter...")
    add_observation_to_encounter(encounter_uuid, new_obs_concept_uuid, new_obs_value, obs_datetime)

    print("Observation update process completed successfully!")

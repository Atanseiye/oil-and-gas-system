import json

def integrate_datasets(well_log_data, seismic_data):
    # Example logic to integrate datasets
    integrated_data = {
        "well_log": well_log_data,
        "seismic_data": seismic_data,
        "combined_info": "Example combined information"
    }
    return integrated_data

# Example usage
with open('well_log.json', 'r') as file:
    well_log_data = json.load(file)

with open('seismic_data.json', 'r') as file:
    seismic_data = json.load(file)

integrated_data = integrate_datasets(well_log_data, seismic_data)
print(json.dumps(integrated_data, indent=2))

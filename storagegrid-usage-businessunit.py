import requests
import csv

# StorageGRID WMI API endpoint and authentication details
api_base_url = 'https://your-storagegrid-url/api/v3'
username = 'your-username'
password = 'your-password'

# Define the business units and their corresponding substrings in tenant names
business_units = {
    'Business Unit A': 'unitA',
    'Business Unit B': 'unitB',
    'Business Unit C': 'unitC',
}

# Create a session and authenticate
session = requests.Session()
auth_url = f'{api_base_url}/authorize'
response = session.get(auth_url, auth=(username, password))
response.raise_for_status()
access_token = response.json()['access_token']
headers = {'Authorization': f'Bearer {access_token}'}

# Create a dictionary to store the usage totals for each business unit
usage_totals = {unit: {'Total Capacity': 0, 'Used Capacity': 0, 'Number of Objects': 0} for unit in business_units}

# Retrieve the list of all tenants
tenants_url = f'{api_base_url}/tenants'
response = session.get(tenants_url, headers=headers)
response.raise_for_status()
tenants = response.json()['data']

# Iterate over the tenants
for tenant in tenants:
    tenant_id = tenant['id']
    tenant_name = tenant['name']

    # Find the matching business unit based on substring match
    matching_unit = None
    for unit, substring in business_units.items():
        if substring in tenant_name:
            matching_unit = unit
            break

    # Skip the tenant if no matching business unit is found
    if not matching_unit:
        continue

    # Retrieve the list of buckets for the tenant
    buckets_url = f'{api_base_url}/tenants/{tenant_id}/buckets'
    response = session.get(buckets_url, headers=headers)
    response.raise_for_status()
    buckets = response.json()['data']

    # Iterate over the buckets
    for bucket in buckets:
        bucket_name = bucket['name']
        bucket_id = bucket['id']

        # Retrieve usage statistics for the bucket
        bucket_url = f'{api_base_url}/usage/buckets/{bucket_id}'
        response = session.get(bucket_url, headers=headers)
        response.raise_for_status()
        usage_data = response.json()['data']

        # Extract relevant usage metrics
        total_capacity = usage_data['total_capacity']
        used_capacity = usage_data['used_capacity']
        num_objects = usage_data['num_objects']

        # Update the usage totals for the matching business unit
        usage_totals[matching_unit]['Total Capacity'] += total_capacity
        usage_totals[matching_unit]['Used Capacity'] += used_capacity
        usage_totals[matching_unit]['Number of Objects'] += num_objects

# Create a CSV file to store the report
csv_file_path = 'storagegrid_usage_report.csv'
with open(csv_file_path, 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)

    # Write headers to the CSV file
    headers = ['Business Unit', 'Total Capacity', 'Used Capacity', 'Number of Objects']
    writer.writerow(headers)

    # Write the usage totals for each business unit to the CSV file
    for unit, totals in usage_totals.items():
        row_data = [unit, totals['Total Capacity'], totals['Used Capacity'], totals['Number of Objects']]
        writer.writerow(row_data)

print(f'Report generated successfully: {csv_file_path}')

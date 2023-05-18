import requests
import csv

# StorageGRID WMI API endpoint and authentication details
api_base_url = 'https://your-storagegrid-url/api/v3'
username = 'your-username'
password = 'your-password'

# Create a session and authenticate
session = requests.Session()
auth_url = f'{api_base_url}/authorize'
response = session.get(auth_url, auth=(username, password))
response.raise_for_status()
access_token = response.json()['access_token']
headers = {'Authorization': f'Bearer {access_token}'}

# Retrieve the list of all tenants
tenants_url = f'{api_base_url}/tenants'
response = session.get(tenants_url, headers=headers)
response.raise_for_status()
tenants = response.json()['data']

# Create a CSV file to store the report
csv_file_path = 'storagegrid_usage_report.csv'
with open(csv_file_path, 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)

    # Write headers to the CSV file
    headers = ['Tenant', 'Bucket', 'Total Capacity', 'Used Capacity', 'Number of Objects']
    writer.writerow(headers)

    # Iterate over the tenants
    for tenant in tenants:
        tenant_id = tenant['id']
        tenant_name = tenant['name']

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

            # Write data to the CSV file
            row_data = [tenant_name, bucket_name, total_capacity, used_capacity, num_objects]
            writer.writerow(row_data)

print(f'Report generated successfully: {csv_file_path}')

import requests
import sys
import os
from dotenv import load_dotenv
from tld import get_fld

# Load environment variables from the .env file
load_dotenv()

# Get the Cloudflare API token from the environment variables
api_token = os.getenv("CLOUDFLARE_API_TOKEN")


def available_zones():
    # Construct the API URL to get available zones
    api_url = "https://api.cloudflare.com/client/v4/zones"

    # Set up the request headers
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json",
    }

    try:
        # Make the GET request to the Cloudflare API to get available zones
        response = requests.get(api_url, headers=headers)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()
            zones = data.get("result", [])

            if zones:
                # print("Available Zones:")
                # for zone in zones:
                    # print(f"Zone Name: {zone['name']}, Zone ID: {zone['id']}")
                return zones
            else:
                print("No zones found in your Cloudflare account.")
                return []
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return []

    except Exception as e:
        print(f"An error occurred: {str(e)}")


def resolve(domain_name, zone_id):
    # Construct the API URL
    api_url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records?type=A&name={domain_name}"

    # Set up the request headers
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json",
    }

    try:
        # Make the GET request to the Cloudflare API
        response = requests.get(api_url, headers=headers)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()
            if data["result"]:
                # Extract and print the A record IP address
                a_record_ip = data["result"][0]["content"]
                print(f"A record IP for {domain_name}: {a_record_ip}")
            else:
                print(f"No A records found for {domain_name}")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    # Check if the user provided a domain_name argument
    if len(sys.argv) != 2:
        print("Usage: python resolve_domain.py <domain_name>")
        sys.exit(1)

    # Get the domain_name from the command line argument
    domain_name = sys.argv[1]

    # Extract the top-level domain (TLD) from the input domain name
    tld = get_fld(f"https://{domain_name}")
    print(f"TLD: {tld}")
    print(f"Domain: {domain_name}")

    for zone in available_zones():
        if zone['name'] == tld:
            resolve(domain_name, zone_id=zone['id'])

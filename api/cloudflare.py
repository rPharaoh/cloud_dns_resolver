import requests

import logging

# Load environment variables from the .env file
from dotenv import load_dotenv
from tld import get_fld
from .common import APIBase

load_dotenv()

# Configure the logger
logging.basicConfig(level=logging.CRITICAL)
logger = logging.getLogger(__name__)


class CloudflareAPI(APIBase):

    api_token = None

    def __init__(self, token=None):
        self.api_token = token

    def available_zones(self):
        # Construct the API URL to get available zones
        api_url = "https://api.cloudflare.com/client/v4/zones"

        # Set up the request headers
        headers = {
            "Authorization": f"Bearer {self.api_token}",
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
                    logger.info("Available Zones:")
                    for zone in zones:
                        logger.info(f"Zone Name: {zone['name']}, Zone ID: {zone['id']}")
                    return zones
                else:
                    logger.info("No zones found in your Cloudflare account.")
            else:
                logger.error(f"Error: {response.status_code} - {response.text}")

        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
        return []

    def resolve(self, domain_name, zone_id):
        # Construct the API URL
        api_url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records?type=A&name={domain_name}"

        # Set up the request headers
        headers = {
            "Authorization": f"Bearer {self.api_token}",
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
                    logger.info(f"A record IP for {domain_name}: {a_record_ip}")
                    return a_record_ip
                else:
                    logger.info(f"No A records found for {domain_name}")
            else:
                logger.error(f"Error: {response.status_code} - {response.text}")
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")

    def query(self, domain_name):
        # Extract the top-level domain (TLD) from the input domain name
        tld = get_fld(f"https://{domain_name}")

        for zone in self.available_zones():
            if zone['name'] == tld:
                ip_address = self.resolve(domain_name=domain_name, zone_id=zone['id'])
                return ip_address

import argparse
import sys

import logging
from api.cloudflare import CloudflareAPI
from dotenv import load_dotenv
from tld import get_fld

# Load environment variables from the .env file
load_dotenv()

# Configure the logger
logging.basicConfig(level=logging.CRITICAL)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    # Check if the user provided a domain_name argument
    if len(sys.argv) != 2:
        logger.info("Usage: python resolve_domain.py <domain_name>")
        sys.exit(1)

    # Create a command-line argument parser
    parser = argparse.ArgumentParser(description="Resolve a domain using Cloudflare API or query AWS Route 53 for DNS records.")
    parser.add_argument("service", choices=["cloudflare", "aws"], help="The DNS resolution service (cloudflare or aws).")
    parser.add_argument("domain", help="The domain name to resolve.")

    # Parse the command-line arguments
    args = parser.parse_args()

    # Get the domain_name from the command line argument
    service = args.service
    domain = args.domain

    # Extract the top-level domain (TLD) from the input domain name
    tld = get_fld(f"https://{domain}")

    logger.info(f"TLD: {tld}")
    logger.info(f"Domain: {domain}")

    cloudflare = CloudflareAPI()
    for zone in cloudflare.available_zones():
        if zone['name'] == tld:
            ip_address = cloudflare.resolve(domain_name=domain, zone_id=zone['id'])
            print(ip_address)

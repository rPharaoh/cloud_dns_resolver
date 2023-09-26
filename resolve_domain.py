import sys

import logging
from api.cloudflare import Cloudflare
from dotenv import load_dotenv
from tld import get_fld

# Load environment variables from the .env file
load_dotenv()

# Configure the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    # Check if the user provided a domain_name argument
    if len(sys.argv) != 2:
        logger.info("Usage: python resolve_domain.py <domain_name>")
        sys.exit(1)

    # Get the domain_name from the command line argument
    domain = sys.argv[1]

    # Extract the top-level domain (TLD) from the input domain name
    tld = get_fld(f"https://{domain}")

    logger.info(f"TLD: {tld}")
    logger.info(f"Domain: {domain}")

    cloudflare = Cloudflare()
    for zone in cloudflare.available_zones():
        if zone['name'] == tld:
            ip_address = cloudflare.resolve(domain_name=domain, zone_id=zone['id'])
            print(ip_address)

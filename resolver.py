import argparse
import os

import logging
from api.cloudflare import CloudflareAPI
from api.aws import AWSAPI
from dotenv import load_dotenv
from tld import get_fld

# Load environment variables from the .env file
load_dotenv()

# Configure the logger
logging.basicConfig(level=logging.NOTSET)
logger = logging.getLogger(__name__)

# Get the Cloudflare API token from the environment variables
api_token = os.getenv("CLOUDFLARE_API_TOKEN")

if __name__ == "__main__":

    # Create a command-line argument parser
    parser = argparse.ArgumentParser(description="Resolve a domain using Cloudflare API or query AWS Route 53 for DNS records.")
    # parser.add_argument("--service", "-s", choices=["cloudflare", "aws"], required=False, help="The DNS resolution service (cloudflare or aws).")
    parser.add_argument("--domain", "-d", help="The domain name to resolve.")

    # Parse the command-line arguments
    args = parser.parse_args()

    # Get the domain_name from the command line argument
    # service = args.service
    domain = args.domain

    # Extract the top-level domain (TLD) from the input domain name
    tld = get_fld(f"https://{domain}")

    logger.info(f"TLD: {tld}")
    logger.info(f"Domain: {domain}")

    cloudflare = CloudflareAPI(api_token)
    result = cloudflare.query(domain_name=domain)
    if result is not None:
        print(result)

    aws = AWSAPI()
    result = aws.query(domain_name=domain)
    if result is not None:
        print(result)

# Function to query DNS records using AWS Route 53
import os

import boto3
import logging

# Load environment variables from the .env file
from dotenv import load_dotenv
from tld import get_fld
from .common import APIBase

load_dotenv()

# Configure the logger
logging.basicConfig(level=logging.NOTSET)
logger = logging.getLogger(__name__)


class AWSAPI(APIBase):

    aws_access_key_id = os.getenv("AWS_ACCESS_KEY")
    aws_secret_access_key = os.getenv("AWS_SECRET_KEY")

    # Function to list available AWS Route 53 hosted zones
    def available_zones(self):
        try:
            # Initialize AWS Route 53 client
            route53 = boto3.client(
                'route53',
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key
            )

            # List hosted zones
            response = route53.list_hosted_zones()

            if 'HostedZones' in response:
                hosted_zones = response['HostedZones']
                if hosted_zones:
                    logger.info("Available AWS Route 53 Hosted Zones:")
                    for zone in hosted_zones:
                        logger.info(f"Zone Name: {zone['Name']}, Zone ID: {zone['Id']}")
                    return hosted_zones
                else:
                    logger.info("No AWS Route 53 hosted zones found in your AWS account.")
            else:
                logger.info("No AWS Route 53 hosted zones found in your AWS account.")

        except Exception as e:
            logger.error(f"An error occurred while listing AWS Route 53 hosted zones: {str(e)}")
        return []

    def resolve(self, domain_name, zone_id):
        try:
            # Initialize AWS Route 53 client
            route53 = boto3.client(
                'route53',
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key
            )

            # Get DNS records for the domain
            response = route53.list_resource_record_sets(
                HostedZoneId=zone_id,
                StartRecordName=domain_name,
                StartRecordType='A',
                MaxItems='1'
            )

            if 'ResourceRecordSets' in response:
                record_set = response['ResourceRecordSets'][0]
                if 'ResourceRecords' in record_set:
                    a_record_ip = record_set['ResourceRecords'][0]['Value']
                    logger.info(f"A record IP for {domain_name} from AWS Route 53: {a_record_ip}")
                    return a_record_ip
                else:
                    logger.info(f"No A records found for {domain_name} in AWS Route 53")
            else:
                logger.info(f"No A records found for {domain_name} in AWS Route 53")

        except Exception as e:
            logger.error(f"An error occurred while querying AWS Route 53: {str(e)}")

    def query(self, domain_name):
        # Extract the top-level domain (TLD) from the input domain name
        tld = get_fld(f"https://{domain_name}")

        for zone in self.available_zones():
            if zone['Name'] == f"{tld}.":
                ip_address = self.resolve(domain_name=domain_name, zone_id=zone['Id'])
                return ip_address

# Cloud DNS Resolver

The **Cloud DNS Resolver** is a Python script that allow you to resolve domain names that are behind Cloudflare or AWS Route 53 useful for domain name with dynamic ip addresses. 
This tool simplifies the process of gathering domain ip address, making it quick and effortless rather than using the gui for each provider.

## Prerequisites

Before you can utilize this script, ensure you have the following prerequisites:

- **Python 3.x**: Make sure you have Python 3.x installed on your system.

- **Required Python Packages**: Install the necessary Python packages using `pipenv`:

    ```bash
    pipenv install
    ```

## Usage

To use this script, follow these steps:

1. Clone this repository to your local machine:

    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2. Create a `.env` file in the same directory as the script, and fill it with the following configurations:

    - `DEBUG=True`: Set this to `True` to enable debugging, or `False` to disable it.

    - `CLOUDFLARE_API_TOKEN`: Replace `your_cloudflare_api_token_here` with your actual Cloudflare API token.

    - `AWS_ACCESS_KEY`: Replace `your_aws_access_key_here` with your AWS access key.

    - `AWS_SECRET_KEY`: Replace `your_aws_secret_key_here` with your AWS secret key.

3. Run the script with the following command:

    ```bash
    python resolver.py --domain <domain_name>
    ```

    Replace `<domain_name>` with the domain you want to resolve.

4. The script will initiate a query using the Cloudflare API to retrieve DNS records for the specified domain. If records are found, it will display the results.

5. If no results are obtained from the Cloudflare API, the script will automatically query AWS Route 53 for DNS records. If records are discovered there, it will display the results.

## Command-line Options

- `--domain` (`-d`): This option allows you to specify the domain name you want to resolve. It is a required argument.

## Example

Here's an example demonstrating how to use the script:

```bash
python resolver.py --domain example.com
```

## Later features
- Adding more providers like GoDaddy, HostGator, Google Cloud
- Make the script as system tool to automatically resolve the ip address with commands like ``` ssh -i key.pem user@example.com ``` a local DNS for short
- Adding caching for hosted zones, that had been resolved before and pass the other domains to a real DNS
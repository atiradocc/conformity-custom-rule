#!/usr/local/bin/python3

import argparse
import sys
import requests
import json

parser = argparse.ArgumentParser(
    description='Lists all custom rules in an organization. See https://cloudone.trendmicro.com/docs/conformity/in-preview-custom-rules-overview/#using-custom-rules')
parser.add_argument('--region', type=str, required=True, choices=[
                    'us-1', 'trend-us-1', 'au-1', 'ie-1', 'sg-1', 'in-1', 'jp-1', 'ca-1', 'de-1'], help='Cloud One Conformity service region')
parser.add_argument('--apiKey', type=str, required=True,
                    help='Full Access Cloud One API Key')
args = parser.parse_args()

header = {
    "Content-Type": "application/vnd.api+json",
    "api-version": "v1",
    "Authorization": "ApiKey {}".format(args.apiKey)
}

payload = {}

conformityEndpoint = "https://conformity.{}.cloudone.trendmicro.com/api/custom-rules".format(
    args.region)

response = requests.get(url=conformityEndpoint, headers=header)

print(response.text)

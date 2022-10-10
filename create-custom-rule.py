#!/usr/local/bin/python3

import argparse
import sys
import requests
import json

parser = argparse.ArgumentParser(
    description='Creates a simple custom rule that validates an S3 bucket name in C1 Conformity. Note: Enabled by default')
parser.add_argument('--name', type=str, required=True,
                    help='Custom Rule Name')
parser.add_argument('--description', type=str, required=True,
                    help='Description')
parser.add_argument('--remediationNotes', type=str, required=True,
                    help='Description')
parser.add_argument('--service', type=str, required=True,
                    help='Conformity Cloud Service')
parser.add_argument('--resourceType', type=str, required=True,
                    help='Conformity Resource Type')
parser.add_argument('--categories', type=str, nargs="+", required=True, choices=[
                    'security', 'cost-optimisation', 'reliability', 'performance-efficiency', 'operational-excellence', 'sustainability'], help='Conformity Well-Architected Pillars')
parser.add_argument('--severity', type=str, required=True, choices=[
                    'LOW', 'MEDIUM', 'HIGH', 'VERY_HIGH', 'EXTREME'], help='Risk Level')
parser.add_argument('--provider', type=str, required=True, choices=[
                    'aws', 'azure', 'gcp'], help='Name of Cloud Provider')
parser.add_argument('--region', type=str, required=True, choices=[
                    'us-1', 'trend-us-1', 'au-1', 'ie-1', 'sg-1'], help='Conformity service region')
parser.add_argument('--apiKey', type=str, required=True,
                    help='Conformity API Key')
args = parser.parse_args()

header = {
    "Content-Type": "application/vnd.api+json",
    "api-version": "v1",
    "Authorization": "ApiKey {}".format(args.apiKey)
}

payload = {
        "name": "{}".format(args.name),
	"description": "{}".format(args.description),
	"remediationNotes": "{}".format(args.remediationNotes),
	"service": "{}".format(args.service),
	"resourceType": "{}".format(args.resourceType),
	"categories": [ 
		"security"
		],
	"severity": "{}".format(args.severity),
	"provider": "{}".format(args.provider),
	"enabled": True,
	"attributes": [
		{
			"name": "bucketName",
			"path": "data.Name",
			"required": True
		}
	],
	"rules": [
		{
			"conditions": {
				"any": [
					{
						"fact": "bucketName",
						"operator": "pattern",
						"value": "^([a-zA-Z0-9_-]){1,32}$"
					}
				]
			},
			"event": {
				"type": "Bucket name is longer than 32 characters"
			}
		}
	]
}

conformityEndpoint = "https://conformity.{}.cloudone.trendmicro.com/api/custom-rules".format(
    args.region)

response = requests.post(url=conformityEndpoint, json=payload, headers=header)

print(response.text)

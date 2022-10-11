#!/usr/local/bin/python3

import argparse
import sys
import requests
import json

parser = argparse.ArgumentParser(
    description='Updates a custom rule in C1 Conformity. See https://cloudone.trendmicro.com/docs/conformity/in-preview-custom-rules-overview/#using-custom-rules')
parser.add_argument('--ruleId', type=str, required=True,
                    help='Conformity Custom Rule Id')
parser.add_argument('--name', type=str, required=True,
                    help='Custom Rule Name')
parser.add_argument('--description', type=str, required=True,
                    help='Description')
parser.add_argument('--eventName', type=str, required=True,
                    help='Real-Time Monitoring Event Name')
parser.add_argument('--remediationNotes', type=str, required=True,
                    help='Remediation Notes for addressing the finding')
parser.add_argument('--service', type=str, required=True,
                    help='Conformity Cloud Service. See https://us-west-2.cloudconformity.com/v1/services')
parser.add_argument('--resourceType', type=str, required=True,
                    help='Conformity Resource Type. See https://us-west-2.cloudconformity.com/v1/resource-types')
parser.add_argument('--categories', type=str, nargs="+", required=True, choices=[
                    'security', 'cost-optimisation', 'reliability', 'performance-efficiency', 'operational-excellence', 'sustainability'], help='Conformity Well-Architected Pillars')
parser.add_argument('--severity', type=str, required=True, choices=[
                    'LOW', 'MEDIUM', 'HIGH', 'VERY_HIGH', 'EXTREME'], help='Risk Level')
parser.add_argument('--provider', type=str, required=True, choices=[
                    'aws', 'azure', 'gcp'], help='C1 Conformity Providers. See https://us-west-2.cloudconformity.com/v1/providers')
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

payload = {
        "name": "{}".format(args.name),
	"description": "{}".format(args.description),
	"remediationNotes": "{}".format(args.remediationNotes),
	"service": "{}".format(args.service),
	"resourceType": "{}".format(args.resourceType),
	"categories": args.categories,
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
				"type": "{}".format(args.eventName)
			}
		}
	]
}

conformityEndpoint = "https://conformity.{0}.cloudone.trendmicro.com/api/custom-rules/{1}".format(
    args.region, args.ruleId)

response = requests.put(url=conformityEndpoint, json=payload, headers=header)

print(response.text)

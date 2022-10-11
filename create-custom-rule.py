#!/usr/local/bin/python3

import argparse
import sys
import requests
import json

def attribute(attributeString):
	dictionary = {}
	for keyValue in attributeString.split(","):
		key,value = keyValue.split(":")
		dictionary[key] = value
	return dictionary

parser = argparse.ArgumentParser(
    description='Creates a custom rule in C1 Conformity. See https://cloudone.trendmicro.com/docs/conformity/in-preview-custom-rules-overview/#using-custom-rules')
parser.add_argument('--name', type=str, required=True,
                    help='Name or title of custom rule')
parser.add_argument('--description', type=str, required=True,
                    help='Description')
parser.add_argument('--eventName', type=str, required=True,
                    help='Real-Time Monitoring Event Name')
parser.add_argument('--remediationNotes', type=str, required=True,
                    help='Notes or steps relevant to remediation. It can also be a URL')
parser.add_argument('--service', type=str, required=True,
                    help='Conformity Cloud Service. See expected values at https://us-west-2.cloudconformity.com/v1/services')
parser.add_argument('--resourceType', type=str, required=True,
                    help='Conformity Resource Type. See expected values at  https://us-west-2.cloudconformity.com/v1/resource-types')
parser.add_argument('--categories', type=str, nargs="*", required=True, choices=[
                    'security', 'cost-optimisation', 'reliability', 'performance-efficiency', 'operational-excellence', 'sustainability'], help='Best Practice Category Pillars')
parser.add_argument('--severity', type=str, required=True, choices=[
                    'LOW', 'MEDIUM', 'HIGH', 'VERY_HIGH', 'EXTREME'], help='Risk/severity level of the custom rule')
parser.add_argument('--provider', type=str, required=True, choices=[
                    'aws', 'azure', 'gcp'], help='C1 Conformity Cloud Providers. See https://us-west-2.cloudconformity.com/v1/providers')
parser.add_argument('--attributes', type=attribute, action='append', required=True,
	help='Collection of user defined attribute names and the associated resource value that will be used as part of the rule logic/evaluation',
	metavar='name:Attribute Name,path:data.JSON Path,required:True|False')
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
	"attributes": args.attributes,
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

conformityEndpoint = "https://conformity.{}.cloudone.trendmicro.com/api/custom-rules".format(
    args.region)

response = requests.post(url=conformityEndpoint, json=payload, headers=header)

print(response.text)

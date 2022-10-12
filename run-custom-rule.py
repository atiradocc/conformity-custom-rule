#!/usr/local/bin/python3

import argparse
import sys
import requests
import json

def dictionary(keyvalues):
	dictionary = {}
	for keyValue in keyvalues.split(","):
		key,value = keyValue.split(":")
		if value.lower() =='true':
			dictionary[key] = True
		elif value.lower() == 'false':
			dictionary[key] = False
		else:
			dictionary[key] = value
	return dictionary

parser = argparse.ArgumentParser(
    description='Dry run a custom rule against a specific resource and account. See https://cloudone.trendmicro.com/docs/conformity/in-preview-custom-rules-overview/#using-custom-rules')
parser.add_argument('--name', type=str, required=True,
                    help='Name or title of custom rule')
parser.add_argument('--description', type=str, required=True,
                    help='Description')
parser.add_argument('--eventName', type=str, required=True,
                    help='Real-Time Monitoring Event Name')
parser.add_argument('--remediationNotes', type=str, required=True,
                    help='Notes or steps relevant to remediation. It can also be a URL')
parser.add_argument('--service', type=str, required=True,
                    help='Conformity Cloud Service. See https://us-west-2.cloudconformity.com/v1/services')
parser.add_argument('--resourceType', type=str, required=True,
                    help='Conformity Resource Type. See https://us-west-2.cloudconformity.com/v1/resource-types')
parser.add_argument('--categories', type=str, nargs="*", required=True, choices=[
                    'security', 'cost-optimisation', 'reliability', 'performance-efficiency', 'operational-excellence', 'sustainability'], help='Best Practice Category Pillars')
parser.add_argument('--severity', type=str, required=True, choices=[
                    'LOW', 'MEDIUM', 'HIGH', 'VERY_HIGH', 'EXTREME'], help='Risk/severity level of the custom rule')
parser.add_argument('--provider', type=str, required=True, choices=[
                    'aws', 'azure', 'gcp'], help='C1 Conformity Cloud Providers. See https://us-west-2.cloudconformity.com/v1/providers')
parser.add_argument('--attributes', type=dictionary, action='append', required=True,
	help='Collection of user defined attribute names and the associated resource value that will be used as part of the rule logic/evaluation',
	metavar='name:Attribute Name,path:data.JSON Path,required:True|False')
parser.add_argument('--ruleLogic', type=str, required=True, choices=[
                    'any', 'all'], help='Determine whether ANY or ALL rulesets must pass for a successful check. See https://cloudone.trendmicro.com/docs/conformity/in-preview-custom-rules-overview/#custom-rule-configuration')
parser.add_argument('--ruleSet', type=dictionary, action='append', nargs="+", required=True,
	help='Conditions ruleset. See https://cloudone.trendmicro.com/docs/conformity/in-preview-custom-rules-overview/#custom-rule-configuration',
	metavar='fact:ATTRIBUTENAME,operator:TESTCRITERIA,value:EXPECTEDVALUE')
parser.add_argument('--rulesetAny', type=dictionary, action='append', nargs="+",
	help='Additional conditions ruletset evaluated using an ANY operator. See https://cloudone.trendmicro.com/docs/conformity/in-preview-custom-rules-overview/#custom-rule-configuration',
	metavar='fact:ATTRIBUTENAME,operator,TESTCRITERIA,value:EXPECTEDVALUE')
parser.add_argument('--rulesetAll', type=dictionary, action='append', nargs="+",
	help='Additional conditions ruletset evaluated using an ALL operator. See https://cloudone.trendmicro.com/docs/conformity/in-preview-custom-rules-overview/#custom-rule-configuration',
	metavar='fact:ATTRIBUTENAME,operator:TESTCRITERIA,value:EXPECTEDVALUE')
parser.add_argument('--resourceId', type=str, required=True,
                    help='Provider resource Id')
parser.add_argument('--accountId', type=str, required=True,
                    help='Conformity Account Id of the account of the resource')
parser.add_argument('--region', type=str, required=True, choices=[
                    'us-1', 'trend-us-1', 'au-1', 'ie-1', 'sg-1', 'in-1', 'jp-1', 'ca-1', 'de-1'], help='Cloud One Conformity service region')
parser.add_argument('--apiKey', type=str, required=True,
                    help='Full Access Cloud One API Key')
args = parser.parse_args()

header = {
    "Content-Type": "application/vnd.api+json",
    "Authorization": "ApiKey {}".format(args.apiKey)
}

payload = {
	"configuration": {
		"name": "{}".format(args.name),
		"description": "{}".format(args.description),
		"remediationNotes": "{}".format(args.remediationNotes),
		"service": "{}".format(args.service),
		"resourceId": "{}".format(args.resourceId),
		"resourceType": "{}".format(args.resourceType),
		"categories": args.categories,
		"severity": "{}".format(args.severity),
		"provider": "{}".format(args.provider),
		"enabled": True,
		"attributes": args.attributes,
		"rules": [ 
			{ "conditions": { "{}".format(args.ruleLogic): args.ruleSet },
			"event": { "type": "{}".format(args.eventName) } } 
			] 
		}
}

if args.rulesetAny is not None:
	payload["rules"][0]["conditions"][args.ruleLogic].append({ "any": args.rulesetAny })

if args.rulesetAll is not None:
	payload["rules"][0]["conditions"][args.ruleLogic].append({ "all": args.rulesetAll })

conformityEndpoint = "https://conformity.{0}.cloudone.trendmicro.com/api/custom-rules/run?accountId={1}".format(
    args.region, args.accountId)

response = requests.post(url=conformityEndpoint, json=payload, headers=header)

print(payload)
print(response.text)

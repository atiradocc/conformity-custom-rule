# conformity-custom-rule

Helps manage custom rules for development purposes in 4 easy-to-use python scripts:

    * create-custom-rule.py
    * get-custom-rule.py
    * update-custom-rule.py
    * delete-custom-rule.py

Additionally, a list-custom-rule.py script allows you to list all rules in an organization.

# conformity terraform provider

The ideal way to create and update custom rules and all things Conformity is to use the Conformity Terraform provider at:

https://registry.terraform.io/providers/trendmicro/conformity/latest/docs

# developing custom rules

The custom rules framework allows creating rich sets of rulesets for evaluating resource configuration.

The run-custom-rule.py script allows obtaining the information known about a resource to assist developing custom rules.

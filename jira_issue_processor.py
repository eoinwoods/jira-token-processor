#!python

##
## jira-issue-processor
##
## This is a self contained Python script that can be used to replace strings in a set of
## Jira issues.  It connects to a Jira instance via the REST API, retrieves all "issues" in
## the project and updates their "description" fields to replace one set of strings with 
## another.
##
## Details in README.md
##
##
from jira import JIRA
import re
from os import environ
from sys import exit

config = {
	"project_name" : "Example Project",
	"jira_url"     : "https://artechra.atlassian.net",
	"replacements" : {
					"www.bbc.co.uk" : "www.itv.co.uk",
					"www.sky.com/project1" : "www.c4.co.uk/c4project"
    }
}

def get_user_and_password_from_env():
	user = environ.get('JIRA_USER')
	password = environ.get('JIRA_PASSWORD')
	return (user, password)

def calculate_issue_updates(issue, replacements):
	ret = None
	description = issue.fields.description
	for from_str, to_str in replacements.items():
		if (description.count(from_str) > 0) :
			exp = re.compile(from_str)
			print("Updating issue " + issue.key + " description, replacing [" + from_str + "] with [" + to_str + "]")
			newDescription = exp.sub(to_str, description)
			print("Old description: [" + description + "] newDescription: [" + newDescription + "]")
			description = newDescription
			ret = (issue, newDescription)
	return ret

def find_and_update_issues(issue_list, string_replacements):
	updates = {}
	for i in issue_list:
		result = calculate_issue_updates(i, string_replacements)
		if (result):
			updates[result[0].key] = result[1]
	print("Updates list: " + str(updates))
	for issue_key in updates.keys():
		issue = jira.issue(issue_key)
		issue.update(description=updates.get(issue_key))
	return len(updates.keys())

def process_issues(jira_instance, jql_query, string_replacements):
	issues = jira.search_issues(jql_query)
	print("Found {} issues".format(len(issues)))

	updated = find_and_update_issues(issues, string_replacements)
	print("Updates complete updated {} issues".format(updated))
	return updated


if __name__=='__main__':
	(user, password) = get_user_and_password_from_env()
	if (not user or not password):
		print("Set $JIRA_USER and $JIRA_PASSWORD to define Jira credentials")
		exit()

	jira = JIRA(basic_auth=(user, password), server=config["jira_url"])
	jql = 'project = "{}" order by key'.format(config["project_name"])
	print("Updating issues in {} that match '{}'".format(config["jira_url"], jql))
	process_issues(jira, jql, config["replacements"])


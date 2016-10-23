from jira import JIRA
import re
from os import environ
from sys import exit

project_name = "Example Project"
jira_url = "https://artechra.atlassian.net"
replacements = {
	"www.bbc.co.uk" : "www.itv.co.uk",
	"www.sky.com/project1" : "www.c4.co.uk/c4project"
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

def find_and_update_issues(issue_list, replacements):
	updates = {}
	for i in issue_list:
		result = calculate_issue_updates(i, replacements)
		if (result):
			updates[result[0].key] = result[1]
	print("Updates list: " + str(updates))
	for issue_key in updates.keys():
		issue = jira.issue(issue_key)
		issue.update(description=updates.get(issue_key))
	return len(updates.keys())

(user, password) = get_user_and_password_from_env()
if (not user or not password):
	print("Set $JIRA_USER and $JIRA_PASSWORD to define Jira credentials")
	exit()

jira = JIRA(basic_auth=(user, password), server=jira_url)

all_project_issues = jira.search_issues('project = "{}" order by key'.format(project_name))
print("Found {} issues".format(len(all_project_issues)))

updated = find_and_update_issues(all_project_issues, replacements)
print("Updates complete updated {} issues in project '{}'".format(updated, project_name))



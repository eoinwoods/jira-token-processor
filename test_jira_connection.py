from jira import JIRA
from os import environ
from sys import exit

user = environ.get('JIRA_USER')
password = environ.get('JIRA_PASSWORD')
if (not user or not password):
	print("Set $JIRA_USER and $JIRA_PASSWORD to define Jira credentials")
	exit()

project_name = "Example Project"
jira_url = "https://artechra.atlassian.net"
issue_key = "EXPRJ-1"

print("Connecting to Jira at {} as {}".format(jira_url, user))
jira = JIRA(basic_auth=(user, password), server=jira_url)

#print("Retrieving issue with key {}".format(issue_key))
#issue = jira.issue(issue_key)
print("Retrieving first issue from project '{}'".format(project_name))
issue_list = jira.search_issues('project = "{}" order by key'.format(project_name), maxResults=1)
assert len(issue_list) > 0

issue = issue_list[0]
print("Issue {} type='{}'' project='{}' summary='{}'".format(issue.key, 
	issue.fields.issuetype.name, issue.fields.project.key, issue.fields.summary))

print("Connection to Jira confirmed")

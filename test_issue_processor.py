# Copyright 2016 Eoin Woods

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from jira import JIRA
from os import environ
import unittest

# The code under test
import jira_issue_processor as proc


project_key = proc.config["project_key"]
jira_url = "https://artechra.atlassian.net"
id_tag = "0xDEADBEEF#"
test_issues = [
	("Issue 1 needing update", """
	Simple update needed on this line for URL www.site1.com
	"""),

	("Issue 2 should not be updated", """
	This issue should not match or be updated www.site2.com
	"""),

	("Issue 3 should be updated", """
	This issue needs an update, but not on this line

	Or this one

	But this line www.site2.com/project1 needs updated
	"""),

	("Issue 4 multi update", """
	This needs an update www.site1.com/project1
	and down here
	this needs an update too www.site1.com/project2
	and again here
	this needs an update www.site2.com/project1 as well
	""")
]
test_replacements = {
	"www.site1.com"          : "wwww.newsite1.com",
	"www.site2.com/project1" : "www.newsite2.com/newproject1",
}



class TestIssueProcessor(unittest.TestCase):

	def create_test_issues(self, jira_instance, project_key, summary_tag):
		count = 0
		for summary, description_text in test_issues:
			summary_text = summary_tag + summary
			jira_instance.create_issue(project=project_key, issuetype="Story", summary=summary_text, description=description_text)
			count += 1
		return count

	def remove_test_issues(self, jira_instance, summary_tag):
		to_delete = jira_instance.search_issues("summary ~ '{}'".format(summary_tag))
		number_to_delete = len(to_delete)
		print("Removing {} issues that match tag '{}'".format(number_to_delete, summary_tag))
		for issue in to_delete:
			issue.delete()
		return number_to_delete

	def setup_test_issues(self, jira_instance, project_key, summary_tag):
		print("Removing any old test issues matching '{}'".format(summary_tag))
		self.remove_test_issues(jira_instance, summary_tag)
		print("Creating test issues tagged with {}".format(summary_tag))
		count = self.create_test_issues(jira_instance, project_key, summary_tag)
		print("Created {} test issues".format(count))
		return count

	def setUp(self):
		user = environ.get('JIRA_USER')
		self.assertTrue(len(user) > 0)
		password = environ.get('JIRA_PASSWORD')
		self.assertTrue(len(password) > 0)
		print("Connecting to Jira at {} as {}".format(jira_url, user))
		self.jira = JIRA(basic_auth=(user, password), server=jira_url)
		count = self.setup_test_issues(self.jira, project_key, id_tag)
		self.assertEqual(count, 4)

	def test_issue_string_replacement(self):
		print("Calling issue processor")
		jql = 'project = "{}" and summary ~ "{}" order by key'.format(project_key, id_tag)
		count = proc.process_issues(self.jira, jql, test_replacements)
		self.assertEqual(count,3, "Wrong number of issues updated by test (expected 3 was {})".format(count))

if __name__ == '__main__':
    unittest.main()

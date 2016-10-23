Jira Token Replacer
===================

This is a simple Python script which allows you to point it at a Jira
repository and project and have it update a set of strings (in fact 
regex'es) to another set of strings (again can be regex'es).

The heavy lifting uses the terrific "jira-python" package to make accessing 
Jira over REST almost trivial.  The package documentation can be found here: 
http://jira.readthedocs.io/

The Python requirements to get this working are stored in the requirements.txt
file which was generated using "pip freeze".

You can create a Python environment to run this with these dependencies using 
the following command line:

   $> pyvenv . && source bin/activate && pip install -r requirements.txt

The snag with using jira-python is that it makes unit testing very difficult
without complex stubbing, so (shamefully) this utility has no tests.

To use the utility:

- Set the JIRA_USER and JIRA_PASSWORD environment variables for a user
  who can update the issues in the project of interest
- Update the script to set the project name and JIRA URL at the top of the
  script
- Update the script to set the set of replacements in the "replacements"
  dictionary variable at the top of the script
- Run the script as "python jira-issue-processor.py" to update the issues
  in the target JIRA system



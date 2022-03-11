#!/usr/bin/env python
from ast import parse
import os
import argparse
import requests
from requests.auth import HTTPBasicAuth
from requests.exceptions import HTTPError

class EnvDefault(argparse.Action):
    def __init__(self, envvar, required=False, default=None, **kwargs):
        if not default and envvar:
            if envvar in os.environ:
                default = os.environ[envvar]
        if required and default:
            required = False
        super(EnvDefault, self).__init__(default=default, required=required, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)

parser = argparse.ArgumentParser(description='Get Jira Release Notes easily', epilog="And that's how we retrieve Jira Release Notes easily!")

### Required Arguments
parser.add_argument('--version', '-v', action=EnvDefault, envvar='JIRA_VERSION_NAME', type=str, required=True, help='The name of the version. Can be specified by environment variable JIRA_VERSION_NAME.')
parser.add_argument('--project', '-p', action=EnvDefault, envvar='JIRA_PROJ', type=int, required=True, help='The ID of the project to which this version is attached. Can be specified by environment variable JIRA_PROJ.')
parser.add_argument('--user', '-u', action=EnvDefault, envvar='JIRA_AUTH_USER', type=str, required=True, help='The Jira authentication user email. Can be specified by environment variable JIRA_AUTH_USER.')
parser.add_argument('--password', action=EnvDefault, envvar='JIRA_AUTH_PASSWORD', type=str, required=True, help='Jira API Authorization Password / API Token. Can be specified by environment variable JIRA_AUTH_PASSWORD.')

### Optional Arguments
# Url
parser.add_argument('--url', action=EnvDefault, envvar='JIRA_URL', type=str, default='https://jira.org', help='The Jira host url. Default value will be https://jira.org. Can be specified by environment variable JIRA_URL.')

# API Version
help_api_version='The Jira API version. Default value is 3. Can be specified by environment variable JIRA_API_VERSION. Supports only versions 2 and 3.'
if "JIRA_API_VERSION" in os.environ:
    parser.add_argument('--api-version', type=int, default=os.environ.get("JIRA_API_VERSION"), help=help_api_version)
else:
    parser.add_argument('--api-version', type=int, default=3, choices=[2, 3], help=help_api_version)

#### Output formatting options

# Release Notes Output Format [text, markdown, html]
help_output_format='The Jira Release Notes Output format. Default value is text. Can be specified by environment variable JIRA_RELEASE_NOTES_OUTPUT_FORMAT. Supports only text, html, markdown.'
if "JIRA_RELEASE_NOTES_OUTPUT_FORMAT" in os.environ:
    parser.add_argument('--format', type=str, default=os.environ.get("JIRA_RELEASE_NOTES_OUTPUT_FORMAT"), help=help_output_format)
else:
    parser.add_argument('--format', type=str, default='text', choices=['text', 'markdown', 'html'], help=help_output_format)

# Skip Intro
help_skip_intro='Skip Output Intro [Version + Issues Count]. Can be specified by environment variable JIRA_RELEASE_NOTES_OUTPUT_SKIP_INTRO. Default value is false.'
if "JIRA_RELEASE_NOTES_OUTPUT_SKIP_INTRO" in os.environ:
    parser.add_argument('--skip-output-intro', type=bool, default=os.environ.get("JIRA_RELEASE_NOTES_OUTPUT_SKIP_INTRO"), help=help_skip_intro)
else:
    parser.add_argument('--skip-output-intro', action='store_true', help=help_skip_intro)

# Skip Version name in Output Intro
help_skip_intro_version_name='Skip Version name in Output Intro. Can be specified by environment variable JIRA_RELEASE_NOTES_OUTPUT_SKIP_INTRO_VERSION_NAME. Default value is false.'
if "JIRA_RELEASE_NOTES_OUTPUT_SKIP_INTRO_VERSION_NAME" in os.environ:
    parser.add_argument('--skip-output-intro-version-name', type=bool, default=os.environ.get("JIRA_RELEASE_NOTES_OUTPUT_SKIP_INTRO_VERSION_NAME"), help=help_skip_intro_version_name)
else:
    parser.add_argument('--skip-output-intro-version-name', action='store_true', help=help_skip_intro_version_name)

# Skip Issues count in Output Intro
help_skip_intro_issues_count='Skip Issues count in Output Intro. Can be specified by environment variable JIRA_RELEASE_NOTES_OUTPUT_SKIP_INTRO_ISSUES_COUNT. Default value is false.'
if "JIRA_RELEASE_NOTES_OUTPUT_SKIP_INTRO_ISSUES_COUNT" in os.environ:
    parser.add_argument('--skip-output-intro-issues-count', type=bool, default=os.environ.get("JIRA_RELEASE_NOTES_OUTPUT_SKIP_INTRO_ISSUES_COUNT"), help=help_skip_intro_issues_count)
else:
    parser.add_argument('--skip-output-intro-issues-count', action='store_true', help=help_skip_intro_issues_count)
    
# Skip Issue type title
help_skip_issue_type_title='Skip Issue type title in Output. Can be specified by environment variable JIRA_RELEASE_NOTES_OUTPUT_SKIP_ISSUE_TYPE_TITLE. Default value is false.'
if "JIRA_RELEASE_NOTES_OUTPUT_SKIP_ISSUE_TYPE_TITLE" in os.environ:
    parser.add_argument('--skip-output-issue-type-title', type=bool, default=os.environ.get("JIRA_RELEASE_NOTES_OUTPUT_SKIP_ISSUE_TYPE_TITLE"), help=help_skip_issue_type_title)
else:
    parser.add_argument('--skip-output-issue-type-title', action='store_true', help=help_skip_issue_type_title)

# Skip issue type new-line
help_skip_newline_between_issue_types='Skip new-line break between Issue types in Output. Can be specified by environment variable JIRA_RELEASE_NOTES_OUTPUT_SKIP_NEWLINE_BETWEEN_ISSUE_TYPES. Default value is false.'
if "JIRA_RELEASE_NOTES_OUTPUT_SKIP_NEWLINE_BETWEEN_ISSUE_TYPES" in os.environ:
    parser.add_argument('--skip-newline-between-issue-types', type=bool, default=os.environ.get("JIRA_RELEASE_NOTES_OUTPUT_SKIP_NEWLINE_BETWEEN_ISSUE_TYPES"), help=help_skip_newline_between_issue_types)
else:
    parser.add_argument('--skip-output-newline-between-issue-types', action='store_true', help=help_skip_newline_between_issue_types)

args = parser.parse_args()

if args.api_version != 2 and args.api_version != 3:
    exit(parser.print_usage())

auth = HTTPBasicAuth(args.user, args.password)
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

def getVersion():
    params = {
        'query': args.version,
        'maxResults': 1
    }

    url = ('%(url)s/rest/api/%(api_version)s/project/%(project)s/version' %{'url': args.url, 'api_version': args.api_version, 'project': args.project})
    try:
        response = requests.get(url, params=params, headers=headers, auth=auth)
        response.raise_for_status()
        # access Json content
        jsonResponse = response.json()
        if jsonResponse["values"] and jsonResponse["values"][0]:
            return jsonResponse["values"][0]
        return None
    except HTTPError as http_err:
        print('HTTP error occurred: {error}' %{'error': http_err})
        exit(1)
    except Exception as err:
        print('Other error occurred: {error}' %{'error': err})
        exit(1)

def getVersionIssues():
    # JQL for filtering version issues
    query = ('project = %(project)s AND fixVersion = "%(version)s" AND resolution IS NOT EMPTY ORDER BY key' %{'project': args.project, 'version': versionName})

    params = {
        'projectId': args.project,
        'maxResults': 1000,
        'jql': query
    }

    url = ('%(url)s/rest/api/%(api_version)s/search' %{'url': args.url, 'api_version': args.api_version})
    try:
        response = requests.get(url, headers=headers, auth=auth, params=params)
        response.raise_for_status()
        return response.json()
    except HTTPError as http_err:
        print('HTTP error occurred: {error}' %{'error': http_err})
        exit(1)
    except Exception as err:
        print('Other error occurred: {error}' %{'error': err})
        exit(1)

def getIssueTypes(issues):
    issueTypes = []
    for issue in issues:
        issueType = issue['fields']['issuetype']['name']
        if issueType not in issueTypes:
            issueTypes.append(issueType)
    issueTypes.sort()
    return issueTypes

# Prints the version name
def printVersionName():
    if args.format == "html":
        print('<h2>' + versionName + '</h2>')
    elif args.format == "markdown":
        print('## ' + versionName)
    else:
        print(versionName)

# Prints the issue type name
def printIssueType(issueType):
    if args.format == "html":
        print('<h4>' + issueType + '</h4>')
    elif args.format == "markdown":
        print('### ' + issueType)
    else:
        print(issueType + ":")

# Prints the issue type name
def printIssues(issueType, issues):
    if args.format == "html":
        if not args.skip_output_issue_type_title:
            print('<h4>' + issueType + '</h4>')
        print('<ul>')
        for issue in issues:
            if issue['fields']['issuetype']['name'] == issueType:
                print('<li>[<a href=\'%(url)s/browse/%(key)s\'>%(key)s</a>] - %(summary)s</li>' %{'url': args.url, 'key': issue['key'], 'summary': issue['fields']['summary']})
        print('</ul>')
    elif args.format == "markdown":
        if not args.skip_output_issue_type_title:
            print('### ' + issueType)
        for issue in issues:
            if issue['fields']['issuetype']['name'] == issueType:
                print('- [[%(key)s](%(url)s/browse/%(key)s)] - %(summary)s' %{'url': args.url, 'key': issue['key'], 'summary': issue['fields']['summary']})
    else:
        if not args.skip_output_issue_type_title:
            print(issueType + ":")
        for issue in issues:
            if issue['fields']['issuetype']['name'] == issueType:
                print('- [%(key)s]: %(summary)s' %{'key': issue['key'], 'summary': issue['fields']['summary']})


def generateReleaseNotes(version, issues):
    if not args.skip_output_intro:
        if not args.skip_output_intro_version_name:
            printVersionName()
        
        if not args.skip_output_intro_issues_count:
            # Print the issues count
            print('%(issues)s total issues.\n' %{'issues': issues['total']})
    
    issueTypes = getIssueTypes(issues['issues'])
    for issueType in issueTypes:
        printIssues(issueType, issues['issues'])

        if not args.skip_output_newline_between_issue_types:
            print('')

version = getVersion()

if version is None:
    print('Ooops! Something went wrong! Unable to retrieve version.')
    exit(2)

versionName = version["name"]
issues = getVersionIssues()

generateReleaseNotes(version, issues)
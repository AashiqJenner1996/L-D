import json 
import requests
import os
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import textwrap


load_dotenv()

JIRA_BASE_URL = os.getenv('JIRA_BASE_URL')
JIRA_API_USER = os.getenv('JIRA_API_USER')
JIRA_API_TOKEN = os.getenv('DRAGON_JIRA_API_TOKEN')
SLACK_WEBHOOK_URL = os.getenv('DRAGON_WEBHOOK_URL')

# Jira filters
FILTERS = {
    "Ready for Start": "38164",
    "In Progress": "38165",
    "Ready for Test": "38167",
    "Ready for Review": "38168",
    "Tickets in Current Sprint also in Backlog": "38170"
}

MAX_PREVIEW_ISSUES = 3


def get_issues(filter_id):
    url = f"{JIRA_BASE_URL}/rest/api/2/search?jql=filter={filter_id}&maxResults={MAX_PREVIEW_ISSUES}"
    
    response = requests.get(
        url,
        auth=HTTPBasicAuth(JIRA_API_USER, JIRA_API_TOKEN),
        headers={'Content-Type': 'application/json'}
    )
    
    if response.status_code != 200:
        print(f"Failed to fetch Jira issues: {response.status_code} - {response.text}")
        return 0, []
    if response.status_code == 200:
        print(f"gottem: {filter_id}")
        
    data = response.json()
    total_issues = data.get('total', 0)
    issues = data.get('issues', [])
    
    formatted_issues = []
    for issue in issues:
        key = issue.get('key')
        summary = issue.get('fields', {}).get('summary') or ""
        summary = textwrap.shorten(summary, width=50, placeholder="...")
        url = f"{JIRA_BASE_URL}/browse/{key}"
        formatted_issues.append(f"• <{url}|{key}> : {summary}")
    
    return total_issues, formatted_issues



def post_to_slack():
    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": ":mag_right: Current Sprint Update :mag_right:"
            }
        }
    ]
    
    for title, filter_id in FILTERS.items():
        count, issues = get_issues(filter_id)
        title_with_count = f"{title} ({count})"
        
        preview_issues = issues[:MAX_PREVIEW_ISSUES]
        issue_text = "\n".join(preview_issues) if preview_issues else "_No issues found._"
        
        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f":arrow_right: *{title_with_count}* :arrow_left: :  \n{issue_text}  \n<https://improbableio.atlassian.net/issues/?filter={filter_id}|*View All Issues*>"
            }
        })
    
    blocks.append({
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "Hi! Here's your sprint update! 🚀"
        }
    })

    slack_data = {"blocks": blocks}
    
    response = requests.post(
        SLACK_WEBHOOK_URL,
        json=slack_data,
        headers={'Content-Type': 'application/json'},
    )

    if response.status_code != 200:
        print(f"Failed to send message: {response.status_code} - {response.text}")
    else:
        print("Slack message posted successfully! ✅")


post_to_slack()

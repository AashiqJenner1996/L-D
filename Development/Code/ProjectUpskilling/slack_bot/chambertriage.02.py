import json 
import requests
import schedule
import time 
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv
import textwrap


load_dotenv()

JIRA_BASE_URL = os.getenv('JIRA_BASE_URL')
JIRA_API_USER = os.getenv('JIRA_API_USER')
JIRA_API_TOKEN = os.getenv('JIRA_API_TOKEN')
SLACK_WEBHOOK_URL = os.getenv('CHAMBER_WEBHOOK_URL')

# Jira filters
FILTERS = {
    "Triage List": "35966",
    "Ready to Merge": "37916",
    "Hot Topics": "37918"
}

def get_issues(filter_id):
    url = f"{JIRA_BASE_URL}/rest/api/2/search?jql=filter={filter_id}&maxResults=3"
    
    response = requests.get(
        url,
        auth=HTTPBasicAuth(JIRA_API_USER, JIRA_API_TOKEN),
        headers={'Content-Type': 'application/json'}
    )
    
    if response.status_code != 200:
        print(f"Failed to fetch Jira issues: {response.status_code} - {response.text}")
        return []
    
    if response.status_code == 200:
        print(f"Gottem")
        data = response.json()
        issues = data.get('issues', [])
        
        # Format issues for Slack
        formatted_issues = []
        for issue in issues:
            key = issue.get('key')
            summary = issue.get('fields', {}).get('summary')
            url = f"{JIRA_BASE_URL}/browse/{key}"
            if summary:
                summary = textwrap.shorten(summary, width=50, placeholder="...")
            formatted_issues.append(f"• <{url}|*{key}*> : {summary}")
        
        return formatted_issues


def post_to_slack():
    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "🔎 A-Sync Triage 🔎"
            }
        }
    ]
    
    for title, filter_id in FILTERS.items():
        issues = get_issues(filter_id)
        issue_text = "\n".join(issues) if issues else "_No issues found._"
        
        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f" :arrow_right: *{title} :arrow_left: :*  \n{issue_text}  \n<https://improbableio.atlassian.net/issues/?filter={filter_id}|*View All Issues*>"
            }
        })
    
    blocks.append({
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "Hi! I've added some previews to our a-sync bug triage, can you think of any other improvements? 🚀"
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

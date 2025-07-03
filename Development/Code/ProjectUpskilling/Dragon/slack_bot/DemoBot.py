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
SLACK_WEBHOOK_URL = os.getenv('DEMO_WEBHOOK_URL')

# Jira filters
FILTERS = {
    "Ready for Test Turnover": "38201",
    "Critical/Blocker Bugs": "38198",
    "Bugs Reported in the last 24 hours": "38197",
    "YUCO Ready for Review": "38168"
}

MAX_PREVIEW_ISSUES = 10


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

def get_issue_description(issue_key):
    url = f"{JIRA_BASE_URL}/rest/api/3/issue/{issue_key}"

    response = requests.get(
        url,
        auth=HTTPBasicAuth(JIRA_API_USER, JIRA_API_TOKEN),
        headers={'Content-Type': 'application/json'}
    )

    if response.status_code != 200:
        print(f"Failed to fetch issue {issue_key}: {response.status_code} - {response.text}")
        return "No description available."

    issue = response.json()
    description_adf = issue.get('fields', {}).get('description', {})

    try:
        lines = []

        for block in description_adf.get('content', []):
            if block.get('type') == 'paragraph':
                line = ''.join(
                    parse_text_emoji_hyperlink(frag)
                    for frag in block.get('content', [])
                ).strip()
                if line:
                    lines.append(line)

            elif block.get('type') == 'bulletList':
                for item in block.get('content', []):
                    paragraph = item.get('content', [])[0]
                    text = ''.join(
                        parse_text_emoji_hyperlink(frag)
                        for frag in paragraph.get('content', [])
                    ).strip()
                    if text:
                        lines.append(f"- {text}")

        return '\n'.join(lines) if lines else "No description available."

    except Exception as e:
        print(f"Error parsing ADF: {e}")
        return "No description available."

def parse_text_emoji_hyperlink(frag):
    if frag.get('type') == 'text':
        text = frag.get('text', '')
        marks = frag.get('marks', [])

        for mark in marks:
            if mark.get('type') == 'link':
                href = mark.get('attrs', {}).get('href')
                if href:
                    return f"<{href}|{text}>"
        return text

    elif frag.get('type') == 'emoji':
        return frag.get('attrs', {}).get('text') or frag.get('attrs', {}).get('shortName', '')

    return ''



def post_to_slack():
    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "QA Daily Report"
            }
        }
    ]

    # --- Add Summary Block from YUCO-441 ---
    issue_key = "YUCO-722"
    description = get_issue_description(issue_key)
    blocks.append({
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": f"{description}"
        }
    })

    # --- Add issue previews by filter ---
    for title, filter_id in FILTERS.items():
        count, issues = get_issues(filter_id)
        title_with_count = f"{title} ({count})"
        
        preview_issues = issues[:MAX_PREVIEW_ISSUES]
        issue_text = "\n".join(preview_issues) if preview_issues else "_No issues found._"
        
        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*{title_with_count}* :arrow_down:  \n{issue_text}  \n<https://improbableio.atlassian.net/issues/?filter={filter_id}|*View All Issues*>"
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

import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import json
import requests
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv

load_dotenv()

JIRA_BASE_URL = os.getenv('JIRA_BASE_URL')
JIRA_API_USER = os.getenv('JIRA_API_USER')
JIRA_API_TOKEN = os.getenv('JIRA_API_TOKEN')
SLACK_WEBHOOK_URL = os.getenv('SLACK_WEBHOOK_URL')

filters = {
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
        return [f"Failed to fetch Jira issues: {response.status_code}"]

    data = response.json()
    issues = data.get('issues', [])

    formatted_issues = []
    for issue in issues:
        key = issue.get('key')
        summary = issue.get('fields', {}).get('summary', 'No summary')
        url = f"{JIRA_BASE_URL}/browse/{key}"
        formatted_issues.append(f"• <{url}|*{key}*> : {summary}")

    return formatted_issues


def post_to_slack():
    blocks = [{"type": "header", "text": {"type": "plain_text", "text": "🔎 A-Sync Triage 🔎"}}]

    for title, filter_id in filters.items():
        issues = get_issues(filter_id)
        issue_text = "\n".join(issues) if issues else "_No issues found._"

        blocks.append({
            "type": "section",
            "text": {"type": "mrkdwn", "text": f"*{title}*\n{issue_text}"}
        })

    slack_data = {"blocks": blocks}

    response = requests.post(
        SLACK_WEBHOOK_URL,
        json=slack_data,
        headers={'Content-Type': 'application/json'}
    )

    if response.status_code != 200:
        messagebox.showerror("Error", f"Failed to send message: {response.status_code}")
    else:
        messagebox.showinfo("Success", "Slack message posted successfully!")


def update_filter():
    key = simpledialog.askstring("Edit Filter", "Enter filter name:")
    value = simpledialog.askstring("Edit Filter", "Enter filter ID:")
    if key and value:
        filters[key] = value
        refresh_filter_list()


def refresh_filter_list():
    listbox.delete(0, tk.END)
    for key, value in filters.items():
        listbox.insert(tk.END, f"{key}: {value}")


# GUI Setup
root = tk.Tk()
root.title("Jira to Slack Poster")
root.geometry("500x400")

listbox = tk.Listbox(root, height=15, width=60)
listbox.pack(pady=10)

refresh_filter_list()

btn_add = tk.Button(root, text="Add/Update Filter", command=update_filter)
btn_add.pack(pady=5)

btn_post = tk.Button(root, text="Post to Slack", command=post_to_slack)
btn_post.pack(pady=5)

root.mainloop()

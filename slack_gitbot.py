# slack_gitbot.py

import os
import requests
import datetime
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# --- Load tokens from env ---
GITHUB_TOKEN = os.getenv("GH_TOKEN")
ORG = "kkr-genweb"

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")  # For Socket Mode

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

# --- GitHub helpers ---
def get_last_week_iso():
    today = datetime.date.today()
    last_week = today - datetime.timedelta(days=7)
    return last_week.isoformat()

def get_all_repos():
    url = f"https://api.github.com/users/{ORG}/repos"
    repos = []
    page = 1
    while True:
        resp = requests.get(url, headers=HEADERS, params={"per_page": 100, "page": page, "type": "public"})
        data = resp.json()
        if not data:
            break
        repos.extend([repo["name"] for repo in data])
        page += 1
    return repos

def get_repo_report(repo):
    commits = get_commits(repo)
    merged, open_prs, closed_prs = get_prs(repo)
    created_issues, closed_issues = get_issues(repo)

    report = f"*Repo:* `{repo}`\n"
    report += f"- Commits (past week): `{commits}`\n"
    report += f"- PRs: Merged=`{merged}`, Open=`{open_prs}`, Closed=`{closed_prs}`\n"
    report += f"- Issues: Created=`{created_issues}`, Closed=`{closed_issues}`"
    return report

def get_commits(repo):
    url = f"https://api.github.com/repos/{ORG}/{repo}/commits"
    params = {"since": get_last_week_iso()}
    resp = requests.get(url, headers=HEADERS, params=params)
    return len(resp.json())

def get_prs(repo):
    url = f"https://api.github.com/repos/{ORG}/{repo}/pulls"
    params = {"state": "all", "per_page": 100}
    resp = requests.get(url, headers=HEADERS, params=params)
    merged, open_prs, closed = 0, 0, 0
    for pr in resp.json():
        if pr["merged_at"] and pr["merged_at"] >= get_last_week_iso():
            merged += 1
        elif pr["state"] == "open":
            open_prs += 1
        elif pr["state"] == "closed" and pr["closed_at"] and pr["closed_at"] >= get_last_week_iso():
            closed += 1
    return merged, open_prs, closed

def get_issues(repo):
    url = f"https://api.github.com/repos/{ORG}/{repo}/issues"
    params = {"since": get_last_week_iso(), "state": "all", "per_page": 100}
    resp = requests.get(url, headers=HEADERS, params=params)
    created, closed = 0, 0
    for issue in resp.json():
        if "pull_request" in issue:
            continue
        if issue["created_at"] >= get_last_week_iso():
            created += 1
        if issue["closed_at"] and issue["closed_at"] >= get_last_week_iso():
            closed += 1
    return created, closed

# --- Slack app ---
app = App(token=SLACK_BOT_TOKEN)

@app.event("app_mention")
def handle_app_mention_events(body, say):
    text = body["event"]["text"]
    user = body["event"]["user"]

    if "list repos" in text.lower():
        repos = get_all_repos()
        blocks = [{
            "type": "section",
            "text": {"type": "mrkdwn", "text": "*Choose a repo:*"}
        }]
        for repo in repos:
            blocks.append({
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": repo},
                        "action_id": "repo_button",
                        "value": repo
                    }
                ]
            })
        say(blocks=blocks)
    else:
        say(f"Hi <@{user}>, I don't recognize that command!")

@app.action("repo_button")
def handle_repo_click(ack, body, say):
    ack()
    repo = body["actions"][0]["value"]
    report = get_repo_report(repo)
    say(report)

# --- Run app ---
if __name__ == "__main__":
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()
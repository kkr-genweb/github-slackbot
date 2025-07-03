# GitHub Slack Bot

A Slack bot that integrates with GitHub to provide repository activity reports directly in Slack. The bot can list repositories and generate reports on commits, PRs, and issues from the past week.

## Features

- List all repositories in your GitHub organization
- Generate activity reports for specific repositories including:
  - Commit count from the past week
  - PR status (merged, open, closed)
  - Issue status (created, closed)
- Simple hello bot example included

## Requirements

- Python 3.12+
- Slack App with Bot Token and Socket Mode enabled
- GitHub Personal Access Token

## Setup with UV

### 1. Install Dependencies

```bash
# Sync dependencies using UV
uv sync
```

### 2. Set Environment Variables

Create a `.env` file in the project root with the following variables that you will get from github and slack:

```
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_APP_TOKEN=xapp-your-app-token
GH_TOKEN=your-github-personal-access-token
```

Alternatively, you can use a script to set these variables in your environment by running `source token_setter.sh` which should set the variables for you using exports per below:
```
export GH_TOKEN="ghp_XXXX"
export SLACK_BOT_TOKEN="xoxb-XXXX"
export SLACK_APP_TOKEN="xapp-XXXX"
```
### 3. Run the Bot

```bash
# Run the main bot
uv run slack_gitbot.py

# Or run the simple hello bot example
uv run hello_slack_bot.py
```

## Slack App Configuration

### ✅ 1. Create your Slack app
1. Visit 👉 https://api.slack.com/quickstart
2. Click "Create an app"
3. Choose "From scratch"
4. Give it a name (e.g., TestBot) and select your workspace
5. Click Create App

### ✅ 2. Enable Socket Mode
Socket Mode lets you run the bot locally without a public URL.
1. On your app's Basic Information page, go to "Socket Mode"
2. Click "Enable Socket Mode"
3. Generate an App-Level Token (click "Generate Token and Scopes")
   - Add scope: `connections:write`
   - Save the generated App Token — it starts with `xapp-`

### ✅ 3. Add Bot Token Scopes
1. Go to "OAuth & Permissions" in the left sidebar
2. Under Scopes → Bot Token Scopes, add:
   - `app_mentions:read` — so your bot can read mentions
   - `chat:write` — so your bot can send messages
   - Add others as needed, like `channels:history` if needed
3. Click "Install App to Workspace" → authorize

This will give you your Bot User OAuth Token — it starts with `xoxb-`

### ✅ 4. Get your tokens
You should now have two tokens:
- Bot Token → `xoxb-...`
- App Token (Socket Mode) → `xapp-...`

Save them as environment variables:
```bash
export SLACK_BOT_TOKEN="xoxb-..."
export SLACK_APP_TOKEN="xapp-..."
```

### ✅ 5. Invite the bot to a channel
In Slack, invite your bot:
```
/invite @YourBotName
```
Without this, the bot won't see events in that channel.

### ✅ 6. (Optional) Subscribe to events
By default, the `app_mentions:read` scope is enough to receive mention events. If you want other events:
1. Go to "Event Subscriptions" → enable
2. For Socket Mode, you don't need to set a public Request URL
3. Add "Subscribe to Bot Events", like:
   - `app_mention`
   - `message.channels`

### ✅ 7. Run your local bot
After setting up your environment variables, run the bot:

```bash
# Run the main bot with UV
uv run slack_gitbot.py
```

### ✅ 8. Test it
In Slack, mention your bot:

```
@YourBotName list repos
```

It should reply with a list of repositories.

### 🔑 Quick Recap

| What | Where |
|------|-------|
| Create App | https://api.slack.com/quickstart |
| Enable Socket Mode | Socket Mode under Basic Info |
| Generate App Token | `xapp-` |
| Add Bot Token Scopes | OAuth & Permissions |
| Install App | Same page — get `xoxb-` |
| Invite Bot | `/invite @bot` |
| Run Locally | `uv run slack_gitbot.py` |

## Usage

Once the bot is running, mention it in any channel with:

- `@YourBot list repos` - Shows a list of repositories with clickable buttons
- Click on any repository button to get a detailed activity report

## Project Structure

- `slack_gitbot.py` - Main bot implementation with GitHub integration
- `hello_slack_bot.py` - Simple example bot for reference
- `token_setter.sh` - Helper script for setting environment variables
- `pyproject.toml` - Project dependencies and metadata

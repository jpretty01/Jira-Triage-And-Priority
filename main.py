# Jeremy Pretty
# JIRA bug Triage and Priority

from jira import JIRA
from datetime import datetime, timedelta
import pytz

# JIRA Authentication
jira_url = "https://yourenvironment.atlassian.net"
username = "your_username"
api_token = "your_api_token"
jira_client = JIRA(jira_url, basic_auth=(username, api_token))

# Fetch new bug reports created in the last 24 hours
current_time = datetime.now(pytz.utc)
twenty_four_hours_ago = current_time - timedelta(days=1)
jql_query = f'project=YOUR_PROJECT_KEY AND issuetype=Bug AND created >= "{twenty_four_hours_ago.strftime("%Y/%m/%d %H:%M")}"'
new_bugs = jira_client.search_issues(jql_query)

# Define a mapping from keywords to assignees
assignee_mapping = {
    'ui': 'ui_team_username',
    'server': 'server_team_username',
    'performance': 'performance_team_username'
}

# Define priority levels based on keywords
priority_mapping = {
    'crash': 'Critical',
    'slow': 'High',
    'minor': 'Low'
}

# Initialize a list to record updates
update_summary = []

# Bug Triage and Assignment Logic
for bug in new_bugs:
    description = bug.fields.description.lower()
    assigned = False
    triaged = False

    # Assignee determination
    for keyword, assignee in assignee_mapping.items():
        if keyword in description:
            try:
                jira_client.assign_issue(bug, assignee)
                update_summary.append(f"Bug ID: {bug.key} assigned to {assignee}")
                assigned = True
                break
            except Exception as e:
                update_summary.append(f"Error updating assignee for Bug ID: {bug.key}: {e}")

    if not assigned:
        update_summary.append(f"No specific keyword found for Bug ID: {bug.key}, consider manual assignment.")

    # Priority determination
    for keyword, priority in priority_mapping.items():
        if keyword in description:
            try:
                jira_client.issue(bug.key).update(fields={'priority': {'name': priority}})
                update_summary.append(f"Bug ID: {bug.key} set to priority {priority}")
                triaged = True
                break
            except Exception as e:
                update_summary.append(f"Error updating priority for Bug ID: {bug.key}: {e}")

    if not triaged:
        update_summary.append(f"No specific keyword found for Bug ID: {bug.key}, consider manual triage for priority.")

# Print the summary of updates
print("\n--- Update Summary ---")
for update in update_summary:
    print(update)

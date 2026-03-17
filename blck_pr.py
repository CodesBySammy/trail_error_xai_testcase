import httpx
import os

async def enforce_pr_gatekeeper(owner: str, repo: str, commit_sha: str, risk_score: float, threshold: float = 30.0):
    """
    Sends a pass/fail status to GitHub based on the Random Forest risk score.
    """
    # 1. The GitHub Status API Endpoint
    url = f"https://api.github.com/repos/{owner}/{repo}/statuses/{commit_sha}"

    # 2. Determine if we should Block or Approve
    if risk_score > threshold:
        state = "failure"  # 🔴 THIS physically turns the check red and blocks the merge
        description = f"Blocked: Risk score {risk_score}% exceeds {threshold}% threshold."
    else:
        state = "success"  # 🟢 THIS turns the check green and allows the merge
        description = f"Cleared: Risk score {risk_score}% is within acceptable limits."

    # 3. Build the Payload
    payload = {
        "state": state,
        "description": description,
        "context": "XAI PR Gatekeeper / Behavioral Risk" # The name that appears on the PR UI
    }

    # 4. Set the Authentication Headers
    # Make sure you have a GitHub Personal Access Token (PAT) saved in your .env file
    headers = {
        "Authorization": f"Bearer {os.getenv('GITHUB_TOKEN')}",
        "Accept": "application/vnd.github.v3+json"
    }

    # 5. Fire the async request to GitHub
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        
    if response.status_code == 201:
        print(f"✅ Successfully updated GitHub Status to: {state}")
    else:
        print(f"❌ Failed to update status. GitHub API returned: {response.text}")

    return response.json()

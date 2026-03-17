"""
Quick test script to verify the PR Gatekeeper status check works on GitHub.

Usage:
  python test_gatekeeper.py <owner/repo> <commit_sha>

Example:
  python test_gatekeeper.py CodesBySammy/trail_error_xai_testcase abc123def

This will:
  1. POST a 🔴 FAILURE status (simulating a high-risk block)
  2. Wait 5 seconds so you can check the PR
  3. POST a 🟢 SUCCESS status (simulating approval)
"""

import sys
import time
import requests
from dotenv import load_dotenv
import os

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def set_status(repo_name: str, sha: str, state: str, description: str):
    url = f"https://api.github.com/repos/{repo_name}/statuses/{sha}"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    payload = {
        "state": state,
        "description": description,
        "context": "XAI PR Gatekeeper"  # Must match your branch protection rule
    }
    
    resp = requests.post(url, json=payload, headers=headers)
    
    print(f"\n{'='*60}")
    print(f"  State:       {state}")
    print(f"  Description: {description}")
    print(f"  HTTP Status: {resp.status_code}")
    
    if resp.status_code == 201:
        print(f"  ✅ Status check posted successfully!")
        data = resp.json()
        print(f"  🔗 View at:  {data.get('url', 'N/A')}")
    else:
        print(f"  ❌ FAILED! Response: {resp.text[:300]}")
    print(f"{'='*60}")
    
    return resp.status_code == 201


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python test_gatekeeper.py <owner/repo> <commit_sha>")
        print("Example: python test_gatekeeper.py CodesBySammy/my-repo abc123def456")
        sys.exit(1)
    
    repo = sys.argv[1]
    sha = sys.argv[2]
    
    print(f"\n🧪 Testing PR Gatekeeper on: {repo} @ {sha[:7]}")
    print(f"   Using token: {GITHUB_TOKEN[:10]}...{GITHUB_TOKEN[-4:]}")
    
    # Step 1: Post a FAILURE (block the merge)
    print("\n🔴 Step 1: Posting FAILURE status (merge should be BLOCKED)...")
    set_status(repo, sha, "failure", "TEST: Merge Blocked — Risk too high (simulated)")
    
    print("\n⏳ Check your PR now — the merge button should be BLOCKED (if branch protection is on).")
    print("   Waiting 10 seconds before posting success...")
    time.sleep(10)
    
    # Step 2: Post a SUCCESS (unblock the merge)
    print("\n🟢 Step 2: Posting SUCCESS status (merge should be ALLOWED)...")
    set_status(repo, sha, "success", "TEST: Cleared — Low risk (simulated)")
    
    print("\n✅ Done! Check your PR again — the check should now be green.")
    print("\n💡 TIP: If the merge button wasn't blocked in Step 1, you need to add")
    print("   'XAI PR Gatekeeper' as a required status check in:")
    print("   GitHub Repo → Settings → Branches → Branch Protection Rules")

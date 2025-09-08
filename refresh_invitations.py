#!/usr/bin/env python3
# Author:  Luke Hindman
# Date: Mon Sep  8 07:17:55 MDT 2025
# Description:  This script walks though all repos within
#     a GitHub organization and any repositories performs
#     the following on any with pending invitations.
# 1. Remove the pending invitation
# 2. Add a new invitation for the same GitHub user with write permissions to the repository.
#
# This process generates a new invite email for the affected user which should enable them to 
#     access the repository.

import requests, os
from datetime import datetime, timedelta, timezone
from decouple import config
GITHUB_TOKEN = config('GITHUB_TOKEN') # PAT with admin:org and repo scopes
ORG = config('ORG')
DRY_RUN = False                          # Set to False to actually make changes
ONLY_LAST_24H = True                    # Set to False to process all repos

API_BASE = "https://api.github.com"
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

def list_org_repos():
    """Return all repositories in the organization (with pagination)."""
    repos = []
    page = 1
    while True:
        url = f"{API_BASE}/orgs/{ORG}/repos?per_page=100&page={page}"
        resp = requests.get(url, headers=HEADERS)
        resp.raise_for_status()
        batch = resp.json()
        if not batch:
            break
        repos.extend(batch)
        page += 1
    return repos

def list_pending_invitations(owner, repo):
    url = f"{API_BASE}/repos/{owner}/{repo}/invitations"
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    return resp.json()

def delete_invitation(owner, repo, invitation_id, username):
    if DRY_RUN:
        print(f"[DRY-RUN] Would delete invitation for {username} in {owner}/{repo}")
        return
    url = f"{API_BASE}/repos/{owner}/{repo}/invitations/{invitation_id}"
    resp = requests.delete(url, headers=HEADERS)
    resp.raise_for_status()

def invite_user(owner, repo, username, permission="write"):
    if DRY_RUN:
        print(f"[DRY-RUN] Would invite {username} to {owner}/{repo} with {permission} permissions")
        return
    url = f"{API_BASE}/repos/{owner}/{repo}/collaborators/{username}"
    payload = {"permission": permission}
    resp = requests.put(url, headers=HEADERS, json=payload)
    resp.raise_for_status()

def refresh_invitations_for_repo(owner, repo):
    pending = list_pending_invitations(owner, repo)
    for inv in pending:
        inv_id = inv["id"]
        username = inv["invitee"]["login"]
        print(f"Refreshing invitation for {username} in {owner}/{repo}...")
        delete_invitation(owner, repo, inv_id, username)
        invite_user(owner, repo, username, permission="write")

def refresh_invitations_for_org():
    repos = list_org_repos()
    cutoff = datetime.now(timezone.utc) - timedelta(days=1)
    for repo in repos:
        repo_name = repo["name"]
        owner = repo["owner"]["login"]
        created_at = datetime.fromisoformat(repo["created_at"].replace("Z", "+00:00"))

        if ONLY_LAST_24H and created_at >= cutoff:
            refresh_invitations_for_repo(owner, repo_name)

if __name__ == "__main__":
    refresh_invitations_for_org()
    mode = "DRY-RUN (no changes made)" if DRY_RUN else "LIVE MODE (changes applied)"
    scope = "last 24h repos only" if ONLY_LAST_24H else "all repos"
    print(f"Completed processing for organization '{ORG}' in {mode}, scope: {scope}.")

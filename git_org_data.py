import os
import requests
from dotenv import load_dotenv

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise ValueError("GITHUB_TOKEN not set")

HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28"
}

def get_org_details(username):
    url = f"https://api.github.com/orgs/{username}"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        raise ValueError(f"Organization '{username}' not found.")
    else:
        raise Exception(f"GitHub API error ({response.status_code}): {response.text}")

def get_org_public_members(username):
    members = []
    page = 1
    per_page = 100

    while True:
        url = f"https://api.github.com/orgs/{username}/public_members"
        params = {"per_page": per_page, "page": page}
        response = requests.get(url, headers=HEADERS, params=params)

        if response.status_code == 200:
            batch = response.json()
            if not batch:
                break
            members.extend(batch)
            page += 1
        elif response.status_code == 404:
            raise ValueError(f"Public members not found for organization '{username}'.")
        else:
            raise Exception(f"GitHub API error ({response.status_code}): {response.text}")

    return members
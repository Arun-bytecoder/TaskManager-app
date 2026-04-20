"""
Run this script AFTER starting uvicorn to add 6 sample tasks.
Usage:
    python add_sample_tasks.py <username> <password>
Example:
    python add_sample_tasks.py venkatO3277 yourpassword
"""
import sys
import urllib.request
import urllib.parse
import json

BASE = "http://localhost:8000"

TASKS = [
    {
        "title": "Set up project repository on GitHub",
        "description": "Create a public repo, push code with clean commit history, add .gitignore and .env.example"
    },
    {
        "title": "Deploy backend to Render",
        "description": "Configure build command, start command, and environment variables on Render dashboard"
    },
    {
        "title": "Write API documentation",
        "description": "Document all endpoints with request/response examples in README.md"
    },
    {
        "title": "Add input validation to registration",
        "description": "Ensure username is 3-20 chars, password is at least 8 chars, email is valid format"
    },
    {
        "title": "Test all CRUD operations end-to-end",
        "description": "Register → Login → Create task → Mark complete → Delete. Verify each step works on live deployment"
    },
    {
        "title": "Review and clean up commit history",
        "description": "Ensure no secrets are committed, remove debug prints, write meaningful commit messages"
    },
]

def request(method, path, data=None, token=None):
    url = BASE + path
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())

def main():
    username = sys.argv[1] if len(sys.argv) > 1 else input("Username: ")
    password = sys.argv[2] if len(sys.argv) > 2 else input("Password: ")

    # Login
    url = BASE + "/login"
    form = urllib.parse.urlencode({"username": username, "password": password}).encode()
    req = urllib.request.Request(url, data=form, method="POST")
    try:
        with urllib.request.urlopen(req) as r:
            token = json.loads(r.read())["access_token"]
    except Exception as e:
        print(f"❌ Login failed: {e}")
        sys.exit(1)

    print(f"✅ Logged in as {username}")

    for i, task in enumerate(TASKS, 1):
        status, data = request("POST", "/tasks", task, token)
        if status == 201:
            print(f"  ✓ Task {i}/6: {task['title']}")
        else:
            print(f"  ✗ Task {i} failed: {data}")

    print("\n🎉 Done! Refresh your browser to see all 6 tasks.")

if __name__ == "__main__":
    main()

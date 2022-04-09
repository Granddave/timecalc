#!/usr/bin/env python3
"""Jira reporting"""

import json
import os
from datetime import datetime

import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv


class JiraTimeReporter:
    server_url = None
    api_token = None

    def __init__(self, server_url: str, username: str, api_token: str):
        self.server_url = server_url
        self.username = username
        self.api_token = api_token

    def report_time(self, issue_key: str, seconds: int):
        load_dotenv()

        rest_path = f"rest/api/3/issue/{issue_key}/worklog"
        payload = json.dumps(
            {
                "timeSpentSeconds": seconds,
                "started": "2022-04-08T08:00:00.000+0000",
            }
        )
        response = requests.request(
            method="POST",
            url=f"{self.server_url}/{rest_path}",
            data=payload,
            auth=HTTPBasicAuth(self.username, self.api_token),
            headers={"Content-Type": "application/json"},
        )

        print(response)
        print(response.text)
        print(
            json.dumps(
                json.loads(response.text),
                sort_keys=True,
                indent=4,
                separators=(",", ": "),
            )
        )


def _main():
    load_dotenv()
    os.getenv("TOKEN")
    jr = JiraTimeReporter(os.getenv("SERVER_URL"), os.getenv("USER_NAME"), os.getenv("API_KEY"))
    jr.report_time("KEY-123", 900)

if __name__ == "__main__":
    _main()

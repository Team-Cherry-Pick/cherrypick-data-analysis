import sys

import requests

from cherrypick_data_analysis.shared.config.env import SLACK_URL

WEB_HOOK_URL = SLACK_URL

def send_slack(text) :
    message = f"[{sys.argv[1]}]\n{text}"

    payload = {"attachments" : [{"text" : message}]} # 접기 기능 등 활성화
    requests.post(WEB_HOOK_URL, json=payload)

def set_PROCESS_NAME(name):
    global _PROCESS_NAME
    _PROCESS_NAME = name
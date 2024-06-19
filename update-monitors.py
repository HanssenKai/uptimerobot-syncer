import os
import sys
import yaml
import requests


def get_uptime_robot_monitors(api_key):
    url = "https://api.uptimerobot.com/v2/getMonitors"
    headers = {"Content-Type": "application/json"}
    payload = {"api_key": api_key, "format": "json"}
    response = requests.post(url, json=payload, headers=headers)
    response_data = response.json()

    monitors_dict = {}
    for monitor in response_data.get('monitors', []):
        monitors_dict[monitor['friendly_name']] = {
            'id': f"{int(monitor['id'])}",
            'url': monitor['url'],
            'method': 'HTTPS',
            'interval': f"{int(monitor['interval']) // 60}m",
            'timeout': '10s'
        }
    return monitors_dict

def sync_monitors(api_key, desired_monitors):
    existing_monitors = get_uptime_robot_monitors(api_key)
    existing_monitors_no_id = {
        key: {subkey: val for subkey, val in value.items() if subkey != 'id'}
        for key, value in existing_monitors.items()
    }
    headers = {"Content-Type": "application/json"}

    

    # Process each desired monitor
    for name, params in desired_monitors.items():
        if name not in existing_monitors:
            # Create monitor
            url = "https://api.uptimerobot.com/v2/newMonitor"
            payload = {
                "api_key": api_key, "format": "json", "type": 1,
                "url": params['url'], "friendly_name": name,
                "interval": int(params['interval'].replace('m', '')) * 60
            }
            response = requests.post(url, json=payload, headers=headers)
            print(f"Created Monitor {name}: {response.json()}")
        elif existing_monitors_no_id[name] != params:
            # Update monitor
            url = "https://api.uptimerobot.com/v2/editMonitor"
            payload = {
                "api_key": api_key, "format": "json", "id": existing_monitors[name]['id'],
                "url": params['url'], "friendly_name": name,
                "interval": int(params['interval'].replace('m', '')) * 60
            }
            response = requests.post(url, json=payload, headers=headers)
            print(f"Updated Monitor {name}: {response.json()}")

    # Check for monitors to delete
    for name in existing_monitors:
        if name not in desired_monitors:
            # Delete monitor
            url = "https://api.uptimerobot.com/v2/deleteMonitor"
            payload = {"api_key": api_key, "format": "json", "id": existing_monitors[name]['id']}
            response = requests.post(url, json=payload, headers=headers)
            print(f"Deleted Monitor {name}: {response.json()}")

if __name__ == "__main__":
    api_key = os.getenv("API_KEY")
    if api_key is None:
        print(f"Error: missing API_KEY environment variable")
        sys.exit(1)
    with open('monitors.yaml', 'r') as file:
        desired_monitors = yaml.safe_load(file)
    sync_monitors(api_key, desired_monitors)

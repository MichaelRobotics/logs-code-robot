import requests
from os import getenv
import json
from urllib3.exceptions import InsecureRequestWarning  # again moduł urlib do wylapywania bledow, rozne certyfikaty

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)  # didable specific warning with certificates


FLEET_IP = "10.1.40.145"
FLEET_PORT = ":443"

class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = f"Bearer {self.token}"
        return r

def get_ip_active_robots():
    try:
        auth_bearer = BearerAuth(getenv('JWT_API_KEY',
                                     'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2NTc2MTU1MjIsIm5iZiI6MTY1NzYxNTUyMiwianRpIjoiYmYzZDY0YmQtOGZmNC00NGZhLWJmZDItZmExZGE0MzhiMDcwIiwiZW1haWwiOiJ2YiIsImZyZXNoIjpmYWxzZSwidHlwZSI6ImFjY2VzcyIsInJvbGVzIjpbIlNVUEVSX1VTRVIiXX0.J917aI2m8vTOFkAD8WjKs7s86fDM5x1nHH9sWwdfaVA'))
        print("log 2")
        response = requests.get(
            f'https://{FLEET_IP}{FLEET_PORT}/api/v1/fleet/robot-specs',
            auth=auth_bearer, verify=False, timeout=50)
        print("log 3")
        response.raise_for_status()  # Raise an exception if the HTTP response status code is not in the 200-299 range
        print("log 4")
    except requests.exceptions.RequestException as e:
        # Handle network-related exceptions (e.g., connection errors, timeouts)
        print(f"RequestException: {e}")
    try:
        workers = response.json()  # Parse the JSON response
        ip_values = [item['ip'] for item in workers]
        print(ip_values)
        print("Api test succesfull!")
    except json.JSONDecodeError as e:
        # Handle JSON parsing errors
        print(f"JSONDecodeError: {e}")
    
def main():
    try:
        # Get Ip from active robots on fleet
        print("log 1")
        get_ip_active_robots()
    except Exception as e:
        print(f"An error occurred when executing main script: {e}")
        # You can also log the exception or take other actions as needed

if __name__ == "__main__":
    main()
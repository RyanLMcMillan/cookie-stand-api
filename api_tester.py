import fire
import requests

# NOTE: Adjust these settings as needed
API_HOST = "http://localhost:8000"
RESOURCE_URI = "cookie_stand"
USERNAME = "admin"
PASSWORD = "admin"


class ApiTester:

    def __init__(self, host=API_HOST):
        self.host = host

    def fetch_tokens(self):


        token_url = f"{self.host}/api/token/"

        response = requests.post(
            token_url, json={"username": USERNAME, "password": PASSWORD}
        )

        data = response.json()

        tokens = data["access"], data["refresh"]

        return tokens

    def get_all(self):

        access_token = self.fetch_tokens()[0]

        url = f"{self.host}/api/v1/{RESOURCE_URI}/"

        headers = {
            "Authorization": f"Bearer {access_token}",
        }

        response = requests.get(url, headers=headers)

        return response.json() or 'No resources'

    def get_one(self, id):

        access_token = self.fetch_tokens()[0]

        url = f"{self.host}/api/v1/{RESOURCE_URI}/{id}"

        headers = {
            "Authorization": f"Bearer {access_token}",
        }

        response = requests.get(url, headers=headers)

        return response.json()

    # TODO adjust parameter names to match API
    def create(self, location, description=None, owner=None):

        access_token = self.fetch_tokens()[0]

        url = f"{self.host}/api/v1/{RESOURCE_URI}/"

        headers = {
            "Authorization": f"Bearer {access_token}",
        }

        data = {
            "location": location,
            "description": description,
            "owner": owner,
        }

        response = requests.post(url, json=data, headers=headers)

        return response.json()

    def update(self, id, name=None, description=None, owner=None):

        access_token = self.fetch_tokens()[0]

        url = f"{self.host}/api/v1/{RESOURCE_URI}/{id}/"

        headers = {
            "Authorization": f"Bearer {access_token}",
        }

        original = self.get_one(id)

        data = {
            "name": name or original["name"],
            "description": description or original["description"],
            "owner": owner or original["owner"],
        }

        response = requests.put(url, json=data, headers=headers)

        return response.text

    def delete(self, id):


        access_token = self.fetch_tokens()[0]

        url = f"{self.host}/api/v1/{RESOURCE_URI}/{id}/"

        headers = {
            "Authorization": f"Bearer {access_token}",
        }

        response = requests.delete(url, headers=headers)

        return response.text


if __name__ == "__main__":
    fire.Fire(ApiTester)
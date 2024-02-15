from fastapi import HTTPException
from config.config import FRONT_END_URL
from config.config import GITHUB_API_URL, REPO_HUB
import requests
from config.config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, GITHUB_API_URL


class AuthRepository:

    def __init__(self):
        self.client_id = CLIENT_ID
        self.client_secret = CLIENT_SECRET
        self.redirect_uri = REDIRECT_URI
        self.front_end_url=FRONT_END_URL
        self.repo_hub=REPO_HUB
        self.github_api_url = GITHUB_API_URL

    def authenticate_user(self, code):
        response = requests.post(
            f"{self.github_api_url}/access_token",
            data={
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "code": code,
                "redirect_uri": self.redirect_uri,
            },
            headers={"Accept": "application/json"},
        )
        data = response.json()

        if "access_token" not in data:
            raise HTTPException(status_code=400, detail="Failed to authenticate")

        access_token = data["access_token"]

        # Use the access_token to make authenticated requests to the GitHub API
        # For example, you can fetch the user's information
        user_response = requests.get(f"{self.repo_hub}/user", headers={"Authorization": f"token {access_token}"})
        user_data = user_response.json()
        username = user_data["login"]

        # Redirect to frontend with the access token and username
        redirect_url = f"{  self.front_end_url}/welcome?access_token={access_token}&username={username}"
        return redirect_url

    def verifiy_the_login(self, token: str):
        # Verify access token by making a request to the GitHub API
        response = requests.get(f"{self.repo_hub}/user", headers={"Authorization": f"token {token}"})
        if response.status_code == 200:
            return True

        return False

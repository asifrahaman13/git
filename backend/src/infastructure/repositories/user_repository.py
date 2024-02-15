# src/infrastructure/repositories/user_repository.py

from bs4 import BeautifulSoup
from fastapi import HTTPException
import requests
from config.config import REPO_HUB


class UserRepository:

    def __init__(self):
        self.repo_hub=REPO_HUB

    def fetch_all_respositories(self, access_token):

        # Fetch repositories of the authenticated user
        repositories_response = requests.get(f"{self.repo_hub}/user/repos", headers={"Authorization": f"token {access_token}"})
        repositories = repositories_response.json()

        extracted_repositories = []
        for repo in repositories:
            extracted_repo = {
                "name": repo["name"],
                "full_name": repo["full_name"],
                "id": repo["id"],
            }
            extracted_repositories.append(extracted_repo)
        return extracted_repositories

    def format_xml_data(self, pom_file_urls):
        dependencies = []
        try:
            for pom_file_url in pom_file_urls:
                pom_file_response = requests.get(pom_file_url)
                pom_file_content = pom_file_response.text
                soup = BeautifulSoup(pom_file_content, "xml")
                for dependency in soup.find_all("dependency"):
                    group_id = dependency.find("groupId").text if dependency.find("groupId") else ""
                    artifact_id = dependency.find("artifactId").text if dependency.find("artifactId") else ""
                    version = dependency.find("version").text if dependency.find("version") else ""
                    if group_id and artifact_id and version:
                        data = {}
                        data["group_id"] = group_id
                        data["artifact_id"] = artifact_id
                        data["version"] = version

                        dependencies.append(data)
                        # dependencies.append(f"{group_id}:{artifact_id} Version {version}")
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Some error occurred")
        return dependencies

    def fetch_all_dependencies(self, access_token, repo):

        # Extract the token part from the Authorization header

        # Verify access token by making a request to the GitHub API
        response = requests.get(f"{self.repo_hub}/user", headers={"Authorization": f"token {access_token}"})

        user = response.json()

        # return response.json()

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to authenticate")
        
        try:

            # Fetch repository content
            repo_content_response = requests.get(
                f"{self.repo_hub}/repos/{user['login']}/{repo.repo_name}/contents",
                headers={"Authorization": f"token {access_token}"},
            )

            if repo_content_response.status_code != 200:
                return
            else:
                print(
                    "The data",
                    repo_content_response.text,
                    repo_content_response.status_code,
                )
                repo_content = repo_content_response.json()

                pom_file_urls = [file["download_url"] for file in repo_content if file["type"] == "file" and file["name"].lower() == "pom.xml"]

                print(pom_file_urls)

                if not pom_file_urls:
                    return {"message": "No pom.xml files found in the repository."}

                dependencies = self.format_xml_data(pom_file_urls)

        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Some error occurred")

        return dependencies

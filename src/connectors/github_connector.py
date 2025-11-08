"""
Connector for GitHub
"""

from typing import Optional

from github import ContentFile, Github, GithubException


class GitHubConnector:
    def __init__(self, token: str):
        """
        Initializes the GitHub Connector.

        Args:
            token (str): The GitHub personal access token.
        """
        self.github = Github(token)

    def get_repo(self, repo_name: str):
        """
        Gets a repository.

        Args:
            repo_name (str): The name of the repository (e.g., "owner/repo").
        """
        try:
            return self.github.get_repo(repo_name)
        except GithubException as e:
            print(f"An error occurred: {e}")
            return None

    def read_file(self, repo_name: str, file_path: str) -> Optional[str]:
        """
        Reads a file from a repository.

        Args:
            repo_name (str): The name of the repository.
            file_path (str): The path to the file in the repository.

        Returns:
            str: The content of the file, or None if an error occurs.
        """
        repo = self.get_repo(repo_name)
        if repo:
            try:
                content: ContentFile = repo.get_contents(file_path)
                return content.decoded_content.decode("utf-8")
            except GithubException as e:
                print(f"An error occurred: {e}")
                return None
        return None

    def create_issue(self, repo_name: str, title: str, body: str):
        """
        Creates an issue in a repository.

        Args:
            repo_name (str): The name of the repository.
            title (str): The title of the issue.
            body (str): The body of the issue.
        """
        repo = self.get_repo(repo_name)
        if repo:
            try:
                return repo.create_issue(title=title, body=body)
            except GithubException as e:
                print(f"An error occurred: {e}")
        return None

    def search_files(self, repo_name: str, query: str):
        """
        Searches for files in a repository.

        Args:
            repo_name (str): The name of the repository.
            query (str): The search query.
        """
        repo = self.get_repo(repo_name)
        if repo:
            try:
                return repo.search_code(query)
            except GithubException as e:
                print(f"An error occurred: {e}")
                return None
        return None

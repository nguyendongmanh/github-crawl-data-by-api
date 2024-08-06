from config import Config

HEADERS = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {Config.GITHUB_TOKEN}",
    "X-GitHub-Api-Version": "2022-11-28",
}

MASTER_OWNER = "ros-industrial"
MASTER_REPO = "universal_robot"

GITHUB_REPO_INFO = "https://api.github.com/repos/{OWNER}/{REPO}"
GITHUB_SEARCH = "https://api.github.com/search"
GITHUB_REPO_TREE = GITHUB_REPO_INFO + "/git/trees/{TREE_SHA}?recursive={recursive}"
GITHUB_REPO_BRANCHES = GITHUB_REPO_INFO + "/branches"
GITHUB_SEARCH_REPOS_BY_TOPIC = (
    GITHUB_SEARCH + "/repositories?q=topic:{TOPIC}&per_page={PER_PAGE}"
)
GITHUB_REPO_CONTENT = GITHUB_REPO_INFO + "/contents/{PATH}"
LANGUAGE_MAPPING = {
    "Python": ".py",
    "C++": ".cpp",
}

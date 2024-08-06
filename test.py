from urllib.parse import urlparse

url = "https://api.github.com/repos/octocat/Hello-World/trees/xxx"

path_parts = urlparse(url).path.split("/")
print(f"{path_parts[2]}/{path_parts[3]}")

from src.utils.utils import get_repo_name, check_file, decode


def extract_info(response):
    items = response["items"]
    total_count = response["total_count"]

    items = [
        {
            f"{item['owner']['login']}/{item['name']}": {
                "star": item["stargazers_count"],
                "default_branch": item["default_branch"],
                "owner": item["owner"]["login"],
                "name": item["name"],
            }
        }
        for item in items
    ]
    return {
        "items": items,
        "total_count": total_count,
    }


def extract_src(response):
    url = response["url"]
    trees = response["tree"]
    files = list(map(lambda x: x["path"], trees))
    filter_files = {f"{file}": "" for file in files if check_file(file)}

    repo_name = get_repo_name(url)

    return repo_name, filter_files


def extract_content(response):
    content = response["content"]
    repo_name = get_repo_name(response["url"])
    return repo_name, response["path"], decode(content)

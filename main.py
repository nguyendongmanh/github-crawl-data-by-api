from config import Config
import asyncio
import aiohttp

# from src.github.fetch_data import extract_data
from src.utils.utils import fetch
from src.github.fetch_data import extract_info, extract_src, extract_content
from setup import *

from pprint import pprint
import json


async def main():
    github_data = []
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        status, master_repo_info_txt = await fetch(
            GITHUB_REPO_INFO.format(OWNER=MASTER_OWNER, REPO=MASTER_REPO),
            session,
            headers=HEADERS,
        )
        if status == 200:
            master_repo_info = json.loads(master_repo_info_txt)
            # pprint(master_repo_info)
            topics = master_repo_info["topics"]
            repo_info_fetchers = [
                asyncio.create_task(
                    fetch(
                        GITHUB_SEARCH_REPOS_BY_TOPIC.format(
                            TOPIC=topic,
                            PER_PAGE=Config.PER_PAGE,
                        ),
                        session,
                        headers=HEADERS,
                    )
                )
                for topic in topics
            ]
            # get items from fetchers
            for done_task in asyncio.as_completed(repo_info_fetchers):
                try:
                    status, response = await done_task
                    response = json.loads(response)
                    if status == 200:
                        github_data.append(extract_info(response))
                    else:
                        print(f"Failed to fetch repos: {status}")
                except Exception as e:
                    print(f"An error occurred: {e}")

            # pprint(github_data[0])
            # get source code of each repository
            repositories = {
                next(iter(item.keys())): next(iter(item.values()))
                for items in (data["items"] for data in github_data)
                for item in items
            }

            tree_repo_fetchers = [
                asyncio.create_task(
                    fetch(
                        GITHUB_REPO_TREE.format(
                            OWNER=repo["owner"],
                            REPO=repo["name"],
                            TREE_SHA=repo["default_branch"],
                            recursive="true",
                        ),
                        session,
                        headers=HEADERS,
                    )
                )
                for repo_name, repo in repositories.items()
            ]

            done, pending = await asyncio.wait(
                tree_repo_fetchers, return_when=asyncio.FIRST_EXCEPTION
            )

            print(f"Tree fetch Done task count: {len(done)}")
            print(f"Tree fetch Pending task count: {len(pending)}")

            for done_task in done:
                if done_task.exception() is None:
                    status, response = done_task.result()
                    response = json.loads(response)
                    if status == 200:
                        repo_name, files = extract_src(response)
                        repositories[repo_name]["src"] = files
                    else:
                        print(f"Failed to fetch repos: {status}")
                else:
                    print(f"An error occurred: {done_task.exception()}")
            # Extract source code
            code_fetchers = [
                asyncio.create_task(
                    fetch(
                        GITHUB_REPO_CONTENT.format(
                            OWNER=repo["owner"],
                            REPO=repo["name"],
                            PATH=path,
                        ),
                        session,
                        headers=HEADERS,
                    )
                )
                for repo_name, repo in repositories.items()
                for path in repo["src"].keys()
            ]

            done, pending = await asyncio.wait(
                code_fetchers, return_when=asyncio.FIRST_EXCEPTION
            )

            print(f"Code fetch Done task count: {len(done)}")
            print(f"Code fetch Pending task count: {len(pending)}")
            for done_task in done:
                if done_task.exception() is None:
                    status, response = done_task.result()
                    response = json.loads(response)
                    if status == 200:
                        repo_name, path, content = extract_content(response)
                        repositories[repo_name]["src"][path] = content
                    else:
                        print(f"Failed to fetch repos: {status}")
                else:
                    print(f"An error occurred: {done_task.exception()}")

            pprint(repositories["ros-industrial/universal_robot"])
        # else:
        #     raise Exception(f"Failed to fetch repo info: {status}")


if __name__ == "__main__":
    asyncio.run(main())

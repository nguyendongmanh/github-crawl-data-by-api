import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(".env"))


class Config:
    GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "ghp_xxxx")
    PER_PAGE = 10
    DEFAULT_PAGE = 1
    SLEEP = 0.1

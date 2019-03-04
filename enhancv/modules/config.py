import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

Config = {
    "proxy_file_path": DATA_DIR + "/proxies.txt",
    "first_names": DATA_DIR + "/first_names.txt",
    "last_names": DATA_DIR + "/last_names.txt",
    "passwords": DATA_DIR + "/passwords.txt",
    "email_providers": DATA_DIR + "/email_providers.txt",
}

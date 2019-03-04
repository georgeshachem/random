import random
import string
from modules.config import Config


def generate_name():
    with open(Config['first_names'], 'r') as file:
        first_names = file.readlines()
    with open(Config['last_names'], 'r') as file:
        last_names = file.readlines()
    return [random.choice(first_names), random.choice(last_names)]


def generate_username(size=12, chars=string.ascii_lowercase + string.digits + random.choice(['_'])):
    return ''.join(random.choice(chars) for _ in range(size))


def generate_password():
    with open(Config['passwords'], 'r') as file:
        passwords = file.readlines()
    return random.choice(passwords)


def generate_email(username):
    with open(Config['email_providers'], 'r') as file:
        email_providers = file.readlines()
    return username + random.choice(email_providers)

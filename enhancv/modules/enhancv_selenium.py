from time import sleep
from selenium import webdriver
import modules.generate_info as accnt
from modules.config import Config
from selenium.webdriver.common.keys import Keys
from fake_useragent import UserAgent


class AccountCreator:
    def __init__(self):
        self.url = 'https://app.enhancv.com/invite/5c7cf215c06951004205357c?utm_source=dynamic&utm_medium=growth&utm_campaign=invite-friends'
        with open(Config['proxy_file_path'], 'r') as file:
            self.proxy = file.readlines()

    def create_account(self):
        for proxy in self.proxy:
            try:
                chrome_options = webdriver.ChromeOptions()
                chrome_options.add_argument("--incognito")
                #chrome_options.add_argument('--proxy-server=%s' % proxy)

                ua = UserAgent()
                userAgent = ua.random
                chrome_options.add_argument(f'user-agent={userAgent}')

                driver = webdriver.Chrome(chrome_options=chrome_options)
                driver.get(self.url)

                name = accnt.generate_name()
                username = accnt.generate_username()
                email = accnt.generate_email(username)
                password = accnt.generate_password()

                sleep(2)

                name_field = driver.find_element_by_xpath('//input[@name="name"]')
                name_field.send_keys(" ".join(name))

                email_field = driver.find_element_by_xpath('//input[@name="email"]')
                email_field.send_keys(email)

                password_field = driver.find_element_by_xpath('//input[@name="password"]')
                password_field.send_keys(password)
                sleep(3)

                driver.find_element_by_xpath('//span[@class="custom-input"]').click()
                sleep(3)

                submit = driver.find_element_by_xpath(
                    '//button[@class="btn btn-lg btn-primary btn-block m-top-4 text-uppercase" and @type="submit"]')
                submit.click()
                # submit.send_keys(Keys.ENTER)
                sleep(5)
            except Exception:
                pass


def run_selenium():
    account = AccountCreator()
    account.create_account()

import json
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from ex_parser.authorization.environ_paths import EnvironPaths
from managers.log_manager import LogManager
from utils import config_parser


def wait_until(delegate, timeout: int):
    end = time.time() + timeout
    while time.time() < end:
        if delegate():
            return True
        else:
            time.sleep(0.1)
    return False


class Authorizer(object):
    def __init__(self, log_manager: LogManager):
        self.cookies = {}
        self.read_cookies()
        self.options = webdriver.ChromeOptions()
        self.environ_paths = EnvironPaths()
        self.log_manager = log_manager
        self.available = False
        self.setup_options()

        self.options.binary_location = self.environ_paths.chrome_bin_path
        self.browser = webdriver.Chrome(options=self.options, executable_path=self.environ_paths.chrome_driver_path)

    def setup_options(self):
        self.options.add_experimental_option('prefs', {
            'profile.default_content_setting_values': {'images': 2, 'plugins': 2, 'popups': 2, 'notifications': 2,
                                                       'auto_select_certificate': 2, 'fullscreen': 2, 'mouselock': 2,
                                                       'mixed_script': 2, 'media_stream': 2, 'media_stream_mic': 2,
                                                       'media_stream_camera': 2, 'automatic_downloads': 2,
                                                       'midi_sysex': 2, 'push_messaging': 2, 'ssl_cert_decisions': 2,
                                                       'metro_switch_to_desktop': 2, 'protected_media_identifier': 2,
                                                       'app_banner': 2, }})
        self.options.add_argument('start-maximized')
        self.options.add_argument('disable-infobars')
        self.options.add_argument('--disable-extensions')
        self.options.add_argument('--headless')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--no-sandbox')

    async def update_session(self):
        await self.log_manager.session_confirm_progress()

        self.browser.get('https://excalibur-craft.ru/index.php?do=login')
        self.browser.find_element_by_xpath('//*[@id="login_name"]').send_keys(
            config_parser.get_section_params('excalibur-craft').get('login'))
        self.browser.find_element_by_xpath('//*[@id="login_password"]').send_keys(
            config_parser.get_section_params('excalibur-craft').get('password'))
        self.browser.find_element_by_xpath('//*[@id="login_password"]').send_keys(Keys.RETURN)

        if not wait_until(lambda: self.browser.current_url == 'https://excalibur-craft.ru/', timeout=10):
            self.available = False
            error_message = self.browser.find_element_by_xpath('//*[@id="ExcaliburPopupWindow"]/div[2]').text
            if 'Вход на сайт не был произведён.' in error_message:
                await self.log_manager.session_confirm_failed()
                self.browser.refresh()
                await self.update_session()
                return
            elif 'Вы достигли максимального количества неудачных попыток авторизации на сайте.' in error_message:
                await self.log_manager.session_confirm_blocked()
                self.browser.close()
                return
        await self.log_manager.session_confirm_success()
        self.available = True
        self.update_cookies()
        self.browser.close()

    def update_cookies(self):
        self.browser.get('https://excalibur-craft.ru/index.php?do=profile&name=Wedyarit')
        for cookie in self.browser.get_cookies():
            self.cookies[cookie['name']] = cookie['value']
        self.save_cookies()

    async def validate(self):
        if not self.is_session_up_to_date():
            await self.update_session()

    def is_session_up_to_date(self):
        return len(self.cookies) > 0 and len(requests.post(url='https://excalibur-craft.ru/engine/ajax/profile/ajax.php',
                                                           data={'action': 'loadProfile', 'user_id': self.cookies['dle_user_id'], 'hash': self.cookies['dle_hash'],
                                                                 'name': config_parser.get_section_params('excalibur-craft').get('login')}, cookies=self.cookies).text) > 5

    def save_cookies(self):
        with open('ex_parser/cookies.json', 'w') as file:
            file.write(json.dumps(self.cookies))

    def read_cookies(self):
        with open('ex_parser/cookies.json', 'r') as file:
            self.cookies = json.loads(file.read())

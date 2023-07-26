from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time

def goto(link):
    driver.get('https://'+link)
    time.sleep(3)
def xpath(s, a='one'):
    if a=='all':
        return driver.find_elements("xpath", s)
    return driver.find_element("xpath", s)
def css_selector(s, a='one'):
    if a=='all':
        return driver.find_elements("css_selector", s)
    return driver.find_element("css_selector", s)

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--headless')
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.1234.567 Safari/537.36")
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_experimental_option(
    "prefs", {"profile.default_content_setting_values.notifications": 1}
)
driver = webdriver.Chrome(options=chrome_options)
driver.set_window_size(340, 620)
# driver = webdriver.Chrome()

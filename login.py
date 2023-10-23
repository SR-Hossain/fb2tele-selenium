from setup_selenium import driver, goto
from selenium.webdriver.common.keys import Keys
try:
    from secret import *
except:
    import os
import time
def login_with_cookies():
    cookies = eval(os.environ['cookies'])
    # with open('cookies.txt', 'r') as f:
        # cookies = eval(f.read())

    for cookie in cookies: # Add the cookies to the current browser session
        driver.add_cookie(cookie)

    # driver.refresh()
    goto('mbasic.facebook.com')
    
    notifications_link = driver.find_element('xpath', "//nav/a[4]")
    

def login_with_pass():
    email_field = driver.find_element("css selector", "input[name='email']")
    email_field.send_keys(os.environ['email_id'])
    
    password_field = driver.find_element("css selector","input[type='password']")
    password_field.send_keys(os.environ['fb_pass'])
    password_field.send_keys(Keys.RETURN)
    # login_button = driver.find_element("xpath", "//input[@value='Log In']")
    # login_button.click()
    try:
        time.sleep(5)
        ok_button = driver.find_element("xpath", "//input[@value='OK']")
        ok_button.click()
    except:
      pass
    cookies = driver.get_cookies()
    # with open('cookies.txt', 'w') as f:
    #     f.write(str(cookies))
    os.environ['cookies'] = str(cookies)
def login():
    goto('mbasic.facebook.com')
    try:
        login_with_cookies()
    except:
        login_with_pass()
    print('Login Complete!!!')
    try:
        print(driver.find_element('tag name', 'body').text)
        
        driver.find_element("css selector","input[value='Continue']").click()
        full_html = driver.page_source
        print(driver.find_element('tag name', 'body').text)
        driver.find_element("css selector","input[value='Continue']").click()
        full_html = driver.page_source
        print(driver.find_element('tag name', 'body').text)
        time.sleep(30)
        driver.find_element("css selector","input[value='Continue']").click()
        full_html = driver.page_source
        print(driver.find_element('tag name', 'body').text)
        
        # Save the HTML content to a file named 'a.html'.
        with open('a.html', 'w', encoding='utf-8') as file:
            file.write(full_html)
        time.sleep(60)
        driver.find_element("css selector","input[value='OK']").click()
        full_html = driver.page_source
        print(driver.find_element('tag name', 'body').text)
        
        # Save the HTML content to a file named 'a.html'.
        with open('a.html', 'w', encoding='utf-8') as file:
            file.write(full_html)
        time.sleep(60)
        login_with_pass()
    except:
        print('emnei hoise')
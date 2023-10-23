from setup_selenium import goto, driver, xpath
import time 
time_slept = 0


def check_for_sust():
    global time_slept
    while True:
        try:
            driver.find_element("partial link text", "SUST CSE").click()
            return
        except:
            time.sleep(10)
            time_slept += 10
            if time_slept >= 3600:
                return




def notification():
    goto('fb.com/notifications')
def click_on_unread():
    while True:
        try:
            xpath("//span[text()='Unread']").click()
            return check_for_sust()
        except:
            time.sleep(1)



def wait_in_unread_for_new_posts():
    global time_slept
    time_slept = 0
    notification()
    click_on_unread()


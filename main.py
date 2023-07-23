from fb import wait_in_unread_for_new_posts
from login import login
from scrap import send_new_posts_to_telegram
import time

login()
while True:
    send_new_posts_to_telegram()
    wait_in_unread_for_new_posts()
time.sleep(560)

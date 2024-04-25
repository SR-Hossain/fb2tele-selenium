import time
from threading import Thread

from fb2tele.settings import env
from .browser import Browser
from .post import Post
from .tele_bot import TeleBot
from bot.models import Post as PostObject


class FB2Tele(Thread):
    @staticmethod
    def facebook_status_code():
        browser = Browser()
        return browser.get_response(url=f"https://mbasic.facebook.com/groups/{env.str('FACEBOOK_GROUP_ID')}/")

    def get_new_post_permalinks(self):
        print(self.get_post_links())
        fetched_post_permalinks = [int(link.split('/')[-2]) for link in self.get_post_links()]
        return list(set(fetched_post_permalinks) - set(self.get_saved_post_permalink_list()))

    @staticmethod
    def get_saved_post_permalink_list():
        links = [post.permalink for post in PostObject.objects.all()]
        print('saved links:', links)
        return links

    @staticmethod
    def get_post_links():
        browser = Browser()
        browser.get_html_data(url=f"https://mbasic.facebook.com/groups/{env.str('FACEBOOK_GROUP_ID')}/")
        return [a['href'][:a['href'].find('?refid')] for a in browser.content.find_all('a', text='Full Story')]

    def run(self):
        tele_bot = TeleBot(
            api_token=env.str('TELEGRAM_API_TOKEN'),
            channel_id=env.str('TELEGRAM_CHAT_ID'),
        )
        for permalink in self.get_new_post_permalinks()[::-1]:
            post = Post(permalink=permalink)
            post.get_html_content()
            try:
                try:
                    post.scrap_post_data()
                except Exception as e:
                    raise Exception("Failed to scrap post from facebook. Error:", e)
                tele_bot.send_message(post)
            except Exception as e:
                tele_bot.send_error_message(e)

            time.sleep(2)

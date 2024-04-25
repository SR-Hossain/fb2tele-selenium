import dataclasses
import re

import requests

from bot.models import Post as PostModel
from fb2tele.settings import env
from .post import Post


@dataclasses.dataclass
class TeleBot:
    def __init__(self, api_token=None, channel_id=None, debug_channel_id=None):
        self.api_token = api_token
        self.channel_id = channel_id
        self.debug_channel_id = debug_channel_id

    def send_error_message(self, e):
        error_message = f'@sr_hossain<pre><code class="language-FIXME">{e}</code></pre>'

        self.send_message_request(error_message, debug=True)

    def send_message(self, post: Post, debug=False):
        message = f'<i><b><a href="{post.url}">{post.sender_name}</a></b></i>'
        if 'Class Routine' in post.text or 'A Section:' in post.text or 'B Section:' in post.text or 'Both Section:' in post.text:
            message += f'<pre><code class="language-Routine">{post.text}</code></pre>'
        else:
            message += f'<pre>Post</pre><b>{post.text}</b>'

            def replace_double_star_with_bold_tag(string):
                pattern = r'\*\*(.*?)\*\*'
                replacement = r'<blockquote>\1</blockquote>'
                modified_string = re.sub(pattern, replacement, string)
                return modified_string

            message += f'<pre>AI Summary</pre><span class="tg-spoiler">{replace_double_star_with_bold_tag(post.summary)}</span>'
        try:
            self.send_message_request(message, debug=debug)
        except Exception as e:
            try:
                self.send_message_request(str(e))
            except Exception as e:
                print("Failed to send error message. Error:", e)
                raise Exception("Failed to send error message. Error:", e)

        if not debug:
            PostModel.objects.create(permalink=post.permalink)
        return self.send_media_message(post, debug=debug)

    def send_message_request(self, text, debug=False):
        response = requests.post(
            url=f"https://api.telegram.org/bot{self.api_token}/sendMessage",
            data={
                'chat_id': self.channel_id if not debug else self.debug_channel_id,
                'text': text,
                'parse_mode': 'html',
                'disable_web_page_preview': True
            }
        )
        if response.status_code != 200:
            raise Exception(f"Failed to send message. Status code: {response.json}")
        return response.status_code

    def send_media_message(self, post: Post, debug=False):
        for media_url in post.media_urls:
            response = requests.post(
                url=f"https://api.telegram.org/bot{self.api_token}/sendPhoto",
                data={
                    'chat_id': self.channel_id if not debug else self.debug_channel_id,
                    'photo': media_url.replace('amp;', ''),
                    'caption': f'<a href="{post.url}">{post.sender_name}</a>',
                    'parse_mode': 'html'
                }
            )
            if response.status_code != 200:
                print("Failed to send media message.", str(response.json))
                self.send_error_message("Failed to send media message, ")
                return 403
            return 200


def test_telebot():
    try:
        telebot = TeleBot(
            api_token=env.str('TELEGRAM_API_TOKEN'),
            channel_id=env.str('TELEGRAM_DEBUG_CHAT_ID'),
            debug_channel_id=env.str('TELEGRAM_DEBUG_CHAT_ID')
        )
        print(dataclasses.asdict(telebot))
        print(telebot.channel_id)
        post = Post(permalink=-1)
        post.url = 'https://google.com'
        post.sender_name = "Test User"
        post.text = "This is a test post."
        post.summary = "This is a test summary."
        post.media_urls = [
            "https://scontent.fdac31-1.fna.fbcdn.net/v/t39.30808-6/438205568_963569812107064_7732825836381661903_n.jpg?stp=cp0_dst-jpg_e15_q65_s240x240&amp;_nc_cat=102&amp;ccb=1-7&amp;_nc_sid=5f2048&amp;efg=eyJpIjoiYiJ9&amp;_nc_ohc=wyN7GHDS_scAb5K34AC&amp;_nc_ht=scontent.fdac31-1.fna&amp;oh=00_AfAXkhexk_ZITB4QOYX_gmQt6toiopbga4B2hEItI19AwQ&amp;oe=662F1184"]

        return telebot.send_message(post=post, debug=True)
    except Exception as e:
        print("Telegram bot Test failed. Error:", e)
        return 400

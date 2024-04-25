import json

from fb2tele.settings import env
from .ai import Gemini
from .browser import Browser


class Post:
    def __init__(self, permalink=None, sender_name=None, text=None, summary=None, media_urls=None):
        self.permalink = permalink
        self.url = f"https://mbasic.facebook.com/groups/{env.str('FACEBOOK_GROUP_ID')}/permalink/{permalink}/"
        self.html_content = None
        self.sender_name = sender_name
        self.text = text
        self.summary = summary
        self.media_urls = media_urls

    def get_html_content(self):
        browser = Browser()
        browser.get_html_data(self.url)
        self.html_content = browser.content.find(id="m_story_permalink_view").find("div")

    def scrap_post_data(self):
        try:
            self.format_post_using_ai()
        except Exception as e:
            print("Failed to format post using AI. Error:", e)
            self.format_post_using_beautifulsoup()

    def format_post_using_ai(self):
        post_element = self.html_content
        ai = Gemini()
        post_data = ai.get_post_json(str(post_element))
        try:
            post_data = json.loads(post_data)
            self.sender_name = post_data['sender_name']
            self.text = post_data['post_text']
            self.summary = post_data['summary']
            self.media_urls = post_data['media_urls']
        except Exception as e:
            print('Failed to load json data')
            raise Exception("Failed to load json data,", e)

    def format_post_using_beautifulsoup(self):
        def get_sender_name():
            sender_name_tag = self.html_content.find("strong")
            if sender_name_tag:
                return sender_name_tag.get_text()
            else:
                print("No <strong> tag found within the element with ID 'm_story_permalink_view'")

        def get_post_text():
            element_with_id = self.html_content

            if element_with_id:
                div_tag = element_with_id.find("div")

                if div_tag:
                    return div_tag.get_text(separator="\n")
                else:
                    print("No <div> tag found within the element with ID 'm_story_permalink_view'")
            else:
                print("No element found with ID 'm_story_permalink_view'")

        def get_media_urls():
            media_urls = []
            for url in self.html_content.select("#m_story_permalink_view > div:nth-child(1) a[href]"):
                if url.startswith('https://mbasic.facebook.com/photo.php?'):
                    media_urls.append(url)
            return media_urls

        self.sender_name = get_sender_name()
        self.text = get_post_text()
        self.media_urls = get_media_urls()


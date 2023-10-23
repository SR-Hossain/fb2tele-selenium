from urllib.parse import unquote
from setup_selenium import driver, goto, xpath, css_selector
try:
    from secret import *
except:
    import os
# from time import sleep
from hash_string import hash
from time import sleep
import tele_bot

def getSender():
    return driver.find_element("id", "m_story_permalink_view").find_element("tag name", "strong").get_attribute("innerText")

def getPost():
    try:
        return str("\n\n"+str(xpath("//meta[@property='og:image:alt']").get_attribute("content")))
    except:
        return ''


def getExtras():
    images = list()
    try:
        extra = css_selector("div[data-ft='{\"tn\":\"H\"}']")
        extra_text = extra.get_attribute("innerText")
    except:
        extra_text = ''
    extra_links = driver.find_elements("xpath", "//div[@id='m_story_permalink_view']/div[1]//a[@href]")
    extra_link = ''
    for link in extra_links:
        link = link.get_attribute('href')
        if 'php?u=' in link:
            link = unquote(link[link.find('=')+1:])
            if 'fbclid' in link:
                link = link[:link.find('fbclid')-1]
            extra_link = '\n<a href="'+link+'">File/Link</a>'
        elif link.startswith('https://mbasic.facebook.com/photo.php?'):
            images.append(link)

    final_images = list()
    for image in images:
        driver.get(image.replace('mbasic','web'))
        # image = xpath("//img[contains(@class, 'img') and starts-with(@src, 'https://scontent')]").get_attribute('src')
        counter = 10
        while counter:
            try:
                image = xpath("//img[@data-visualcompletion='media-vc-image']")
                image = image.get_attribute('src')
                counter = 0
                final_images.append(image)
            except:
                sleep(1)
                counter -= 1
    return [final_images, extra_text+extra_link]

def fetch(permalink, saved_posts):
    post = dict()
    goto('mbasic.facebook.com/groups/'+os.environ['group_link']+'/permalink/'+str(permalink))
    post['link'] = permalink
    post['text'] = getPost()
    post['hash'] = str(hash(post['text']))
    # print(post)
    if post['link'] in saved_posts and saved_posts[post['link']]==post['hash']:
        return None
    post['sender'] = getSender() + ' [Jump To Post ↗]'
    extra = getExtras()
    post['extra'] = extra[1]
    post['image'] = extra[0]
    if post['link'] in saved_posts:
        post['extra'] += '\n#updated_post'
    # tele_bot.sendPost(post)
    return post
    
    
    
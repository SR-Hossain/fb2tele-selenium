from setup_selenium import driver, goto, xpath, css_selector
try:
    from secret import *
except:
    import os
from time import sleep
from fetch import fetch
import tele_bot, sms_bot
import json

def get_permalinks():
    goto('mbasic.facebook.com/'+os.environ['group_link'])
    sleep(4)
    # link_elements = xpath("//a[abbr]", 'all')
    link_elements = driver.find_elements("link text", "Full Story")
    permalinks = []


    for link_element in link_elements:
        link = link_element.get_attribute('href')
        last_index = link.find('?')-1
        link = link[:last_index]
        # we need post integer only
        link = link.split('/')[-1]
        try:
            permalinks.append(str(int(link)))
        except:
            pass

    return list(reversed(permalinks[1:8]))


    

def load_saved_posts():
    prev_posts = dict() 
    try:
        prev_posts = dict(json.load(open('posts.json')))
    except: 
        print('prev post ashe nai dict e')
    return prev_posts

def save_post(saved_posts):
    with open('posts.json', 'w') as ps:
        json.dump(dict(list(saved_posts.items())[-1000:]), ps)
    
    
# def fetched_posts():
    

def send_new_posts_to_telegram():
    # saved_posts = load_saved_posts()
    # for post in fetched_posts():
    #     if post['link'] in saved_posts:
    #         if saved_posts[post['link']]==post['hash']:
    #             continue
    #         post['extra'] += '\n#updated_post'
    #     # print(post)
    #     tele_bot.sendPost(post)
    #     saved_posts[post['link']]=post['hash']
    # save_post(saved_posts)
    saved_posts = load_saved_posts()
    for link in get_permalinks():
        post = fetch(link, saved_posts)
        if post != None:
            tele_bot.sendPost(post)
            sms_bot.sendPost(post)
            saved_posts[post['link']] = post['hash']
    save_post(saved_posts)
  
    # save_post(fetched_posts())


    

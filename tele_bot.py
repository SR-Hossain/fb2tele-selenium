# import urllib.parse
import time
try:
    from secret import *
except:
    import os
import telegram

bot_api = os.environ['bot_api']
chat_id = os.environ['chat_id']

bot = telegram.Bot(token = bot_api)


def sendMsg(text):
    i = 0
    l = len(text)
    while i<l:
        time.sleep(5)
        txt = text[i:i+2000]
        #txt = urllib.parse.quote(txt)
        try:
            bot.send_message(chat_id, txt, 'html', disable_web_page_preview=True)
        except Exception as e:
            print(str(e))
        i+=2000

def sendPhoto(text, imgs):
    imgs[0] = telegram.InputMediaPhoto(str(imgs[0]), caption=text, parse_mode = 'html')
    for i in range(1,len(imgs)):
        imgs = telegram.InputMediaPhoto(str(imgs[i])) 
    bot.send_media_group(chat_id, imgs) 


def sendPost(post):
    try:
        text = '<a href="'+post['link']+'">' + post['sender'] + '</a>\n\n' + post['text']
        if 'extra' in post:
            text += '\n\n\n'+post['extra']
        if 'image' in post:
            try:
                sendPhoto(text, post['image'])
            except:
                sendMsg(text)
        else:
            sendMsg(text)
    except:
        print('Tele te msg jay nai...')
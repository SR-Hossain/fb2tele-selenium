# import urllib.parse
import time
try:
    from secret import *
except:
    import os
import telegram
import asyncio

bot_api = os.environ['bot_api']
chat_id = os.environ['chat_id']

bot = telegram.Bot(token=bot_api)

async def sendMsg(text):
    for i in range(0, len(text), 2000):
        time.sleep(5)
        # txt = urllib.parse.quote(txt)
        try:
            await bot.send_message(chat_id, text[i:i + 2000], parse_mode='html', disable_web_page_preview=True)
        except Exception as e:
            print(str(e))

async def sendPhoto(imgs, text):
    # Convert the first image to an InputMediaPhoto with a caption
    imgs[0] = telegram.InputMediaPhoto(str(imgs[0]), caption=text, parse_mode='HTML')

    # Create a list to store all the media objects
    media_group = [imgs[0]]

    # Convert the rest of the images to InputMediaPhoto objects
    for i in range(1, len(imgs)):
        media_group.append(telegram.InputMediaPhoto(str(imgs[i])))

    # Send the media group
    await bot.send_media_group(chat_id, media_group)

async def main(post):
    sender = '<a href="https://fb.com/groups/'+os.environ['group_link']+'/permalink/'+post['link']+'">' + post['sender'] + '</a>'
    txt = post['text']
    txt += post['extra']
    if len(txt)>0:
        await sendMsg(sender + txt)
    if len(post['image'])>0:
        await sendPhoto(post['image'], sender)




def sendPost(post):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(post))

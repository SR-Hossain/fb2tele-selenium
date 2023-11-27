# import urllib.parse
import time
import aiohttp
try:
    from secret import *
except:
    import os
import asyncio

from gptit import shorten_text

sms_api = os.environ['sms_api_token']
receivers = os.environ['receiver_phone_number'].split(',')
senderid = os.environ['sender_id']

def process_text(text):
    cnt = 0
    i = 0
    text = '\n'.join([x.strip() for x in text.split('\n') if len(x.strip())>0])
    while i < len(text):
        if text[i].isdigit():
            cnt += 1
        elif text[i].isalpha():
            cnt = 0
        if cnt == 3:
            text = text[:i] + '|' + text[i:]
            i += 1
            cnt = 0
        i += 1
    
    return text

async def sendMsg(text, extra, receiver):
    if len(text) > 640: text = text[:640] + '...'
    # txt = urllib.parse.quote(txt)
    try:
        msg = process_text(shorten_text(text))
        url = 'http://api.smsinbd.com/sms-api/sendsms'
        body = {
            'api_token': sms_api,
            'contact_number': receiver,
            'senderid': senderid,
            'message': msg
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=body) as response:
                print(await response.text())

    except Exception as e:
        print(str(e))

async def main(post):
    sender = post['sender']
    sender = sender[:sender.find('[')]
    txt = post['text']
    # txt += post['extra']
    if len(txt)>0:
        for receiver in receivers:
            await sendMsg(sender + txt, post['extra'], receiver)


def sendPost(post):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(post))

def testMsg():
    loop = asyncio.get_event_loop()
    txt = """
    যাদের সোসাইটি ফি জমা দেয়া হয়েছে তাদের লিস্ট।আমার কাছে এখনো ১/১ এবং ১/২ এর লিস্টটা আসেনি।তাই ঐটা এখনো আপডেট করিনি।পরিক্ষার আগে সবাই সোসাইটি ফি ৬০০ টাকা করে ৩৪০৫০৫৩৫ এই হিসাব নাম্বারে জমা দিয়ে স্লিপ আমার কাছে জমা দিস।
society fee - Google Drive
    """
    loop.run_until_complete(sendMsg(txt, ''))

if __name__ == '__main__':
    testMsg()
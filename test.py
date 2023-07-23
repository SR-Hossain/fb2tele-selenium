try:
    from secret import *
except:
    import os
import time
import telegram

bot_api = os.environ['bot_api']
chat_id = os.environ['chat_id']

bot = telegram.Bot(token=bot_api)


async def sendMsg(text):
    i = 0
    l = len(text)
    while i < l:
        time.sleep(5)
        txt = text[i:i + 2000]
        try:
            await bot.send_message(chat_id, txt, parse_mode='HTML', disable_web_page_preview=True)
        except Exception as e:
            print(str(e))
        i += 2000


# Usage example:
post_data = {
    'link': 'https://example.com',
    'sender': 'Sender Name',
    'text': 'This is the main text of the post.',
    'extra': 'Additional information (optional)',
    'image': []
}

# To call an async function, you need an event loop, like this:
import asyncio
loop = asyncio.get_event_loop()
loop.run_until_complete(sendMsg(post_data['text']))

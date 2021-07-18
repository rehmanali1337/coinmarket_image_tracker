from telethon import TelegramClient, events, types
import json
import logging
import asyncio
import socks
import os
from exts.monitor import LinkMonitor
import multiprocessing as mp
import wget


logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.ERROR)

config = json.load(open('config.json'))

BOT_TOKEN = config.get("TELEGRAM_BOT_TOKEN")

if not os.path.exists('sessionFiles'):
    os.mkdir('sessionFiles')
proxy = {
    'proxy_type': socks.PROXY_TYPE_SOCKS5,
    'addr': '45.94.47.18',
    'port': 8062,
    'username': 'unergtzc-dest',
    'password': 'vc3h2h86oht1'
}

bot = TelegramClient('sessionFiles/bot',
                     config.get("TELEGRAM_API_ID"), config.get("TELEGRAM_API_HASH"), proxy=proxy)


async def on_ready():
    wait_time = 0.5
    if not bot.is_connected() or await bot.is_user_authorized():
        await asyncio.sleep(wait_time)
    bot.parse_mode = 'md'
    queue = mp.Queue()
    monitor = LinkMonitor(queue)
    mp.Process(target=monitor.start).start()
    channel_id = config.get("OUTPUT_CHANNEL_ID")
    assert channel_id is not None
    peer = types.PeerChannel(channel_id)
    print('Bot is ready!')
    while True:
        while queue.empty():
            await asyncio.sleep(0.1)
        details = queue.get(block=False)
        image_url = details[0]
        image_name = image_url.split('/')[-1]
        google_search_url = details[1]
        image_loc = f'./{image_name}'
        wget.download(image_url, image_loc)
        message = f'Image link : {image_url}\nClick [Here]({google_search_url}) to go to google image search results!'
        await bot.send_message(peer, message, file=image_loc)
        os.remove(image_loc)


try:
    bot.start(bot_token=BOT_TOKEN)
    bot.loop.create_task(on_ready())
    bot.run_until_disconnected()
except KeyboardInterrupt:
    print('Quiting bot ...')
    exit()

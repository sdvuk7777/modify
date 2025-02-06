# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

import os
import re
import sys
import json
import time
import asyncio
import requests
import subprocess
from datetime import datetime, timedelta

import core as helper
from utils import progress_bar
from vars import API_ID, API_HASH, BOT_TOKEN
from aiohttp import ClientSession
from pyromod import listen
from subprocess import getstatusoutput

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from pyrogram.errors.exceptions.bad_request_400 import StickerEmojiInvalid
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Global variables for user limits
MAX_USERS = 5
MAX_LINKS_PER_USER = 20
active_users = {}
user_daily_limits = {}
last_reset_time = datetime.now()

bot = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

def reset_daily_limits():
    """Reset daily limits at midnight"""
    global user_daily_limits, last_reset_time
    current_time = datetime.now()
    
    # Reset limits if it's a new day
    if current_time.date() > last_reset_time.date():
        user_daily_limits = {}
        last_reset_time = current_time

@bot.on_message(filters.command(["start"]))
async def start(bot: Client, m: Message):
    reset_daily_limits()
    await m.reply_text(f"<b>Hello {m.from_user.mention} 👋\n\n I Am A Bot For Download Links From Your **.TXT** File And Then Upload That File On Telegram So Basically If You Want To Use Me First Send Me /upload Command And Then Follow Few Steps..\n\nUse /stop to stop any ongoing task.</b>")

@bot.on_message(filters.command("stop"))
async def restart_handler(_, m):
    await m.reply_text("**Stopped**🚦", True)
    os.execl(sys.executable, sys.executable, *sys.argv)

@bot.on_message(filters.command(["upload"]))
async def upload(bot: Client, m: Message):
    reset_daily_limits()
    user_id = m.from_user.id

    # Check if the user has exceeded daily limit
    if user_id in user_daily_limits:
        if user_daily_limits[user_id] >= MAX_LINKS_PER_USER:
            await m.reply_text(f"**You have reached your daily limit of {MAX_LINKS_PER_USER} links. Please try again tomorrow.**")
            return

    # Check if the bot is busy with maximum users
    if len(active_users) >= MAX_USERS:
        user_list = list(active_users.keys())
        try:
            user_names = [f"@{(await bot.get_users(uid)).username}" for uid in user_list]
        except Exception:
            user_names = [str(uid) for uid in user_list]
        
        await m.reply_text(f"**Server is currently processing requests for {len(active_users)} users:** {', '.join(user_names)}.\n\n**Please wait and try again in a few moments.**")
        return

    # Add user to active users with a unique identifier
    active_users[user_id] = {
        'start_time': datetime.now(),
        'username': m.from_user.username or m.from_user.first_name
    }

    try:
        editable = await m.reply_text('𝕤ᴇɴᴅ ᴛxᴛ ғɪʟᴇ ⚡️')
        input: Message = await bot.listen(editable.chat.id)
        x = await input.download()
        await input.delete(True)

        path = f"./downloads/{m.chat.id}"

        try:
            with open(x, "r") as f:
                content = f.read()
            content = content.split("\n")
            links = []
            for i in content:
                # Safely handle links that might not have "://"
                link_parts = i.split("://", 1)
                if len(link_parts) == 2:
                    links.append(link_parts)
                elif len(link_parts) == 1 and link_parts[0].strip():
                    links.append(["", link_parts[0]])
            os.remove(x)
        except Exception as file_error:
            await m.reply_text(f"**Invalid file input:** {str(file_error)}")
            if os.path.exists(x):
                os.remove(x)
            return

        # Check if the file contains master.mpd links
        has_master_mpd = False
        try:
            has_master_mpd = any("/master.mpd" in (link[1] if len(link) > 1 else "") for link in links)
        except Exception:
            pass

        if has_master_mpd:
            await editable.edit("**𝑵𝒐𝒘 𝒔𝒆𝒏𝒅 𝒚𝒐𝒖𝒓 𝑷𝑾 𝒖𝒔𝒆𝒍𝒆𝒔𝒔 𝒂𝒄𝒕𝒊𝒗𝒆 𝒕𝒐𝒌𝒆𝒏.**")
            token_input: Message = await bot.listen(editable.chat.id)
            token = token_input.text
            await token_input.delete(True)

        await editable.edit(f"**𝕋ᴏᴛᴀʟ ʟɪɴᴋ𝕤 ғᴏᴜɴᴅ ᴀʀᴇ🔗🔗** **{len(links)}**\n\n**𝕊ᴇɴᴅ 𝔽ʀᴏᴍ ᴡʜᴇʀᴇ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ ɪɴɪᴛɪᴀʟ ɪ𝕤** **1**")
    input0: Message = await bot.listen(editable.chat.id)
    raw_text = input0.text
    await input0.delete(True)

    await editable.edit("**Now Please Send Me Your Batch Name**")
    input1: Message = await bot.listen(editable.chat.id)
    raw_text0 = input1.text
    await input1.delete(True)

    await editable.edit("**𝔼ɴᴛᴇʀ ʀᴇ𝕤ᴏʟᴜᴛɪᴏɴ📸**\n144,240,360,480,720,1080 please choose quality")
    input2: Message = await bot.listen(editable.chat.id)
    raw_text2 = input2.text
    await input2.delete(True)
    try:
        if raw_text2 == "144":
            res = "256x144"
        elif raw_text2 == "240":
            res = "426x240"
        elif raw_text2 == "360":
            res = "640x360"
        elif raw_text2 == "480":
            res = "854x480"
        elif raw_text2 == "720":
            res = "1280x720"
        elif raw_text2 == "1080":
            res = "1920x1080"
        else:
            res = "UN"
    except Exception:
        res = "UN"

    await editable.edit("Now Enter A Caption to add caption on your uploaded file")
    input3: Message = await bot.listen(editable.chat.id)
    raw_text3 = input3.text
    await input3.delete(True)
    highlighter = f"️ ⁪⁬⁮⁮⁮"
    if raw_text3 == 'Robin':
        MR = highlighter
    else:
        MR = raw_text3

    await editable.edit("Now send the Thumb url\nEg » https://iili.io/2LBPdRj.md.jpg \n Or if don't want thumbnail send = no")
    input6 = message = await bot.listen(editable.chat.id)
    raw_text6 = input6.text
    await input6.delete(True)
    await editable.delete()

    thumb = input6.text
    if thumb.startswith("http://") or thumb.startswith("https://"):
        getstatusoutput(f"wget '{thumb}' -O 'thumb.jpg'")
        thumb = "thumb.jpg"
    else:
        thumb == "no"

    if len(links) == 1:
        count = 1
    else:
        count = int(raw_text)

    try:
        for i in range(count - 1, len(links)):
            # Update user's daily limit
            if user_id in user_daily_limits:
                user_daily_limits[user_id] += 1
            else:
                user_daily_limits[user_id] = 1

            # Check if user has reached daily limit
            if user_daily_limits[user_id] > MAX_LINKS_PER_USER:
                await m.reply_text("**You have reached your daily limit of 20 links.**")
                break

            V = links[i][1].replace("file/d/", "uc?export=download&id=").replace("www.youtube-nocookie.com/embed", "youtu.be").replace("?modestbranding=1", "").replace("/view?usp=sharing", "")

            # Handle new master.mpd URLs
            if "/master.mpd" in V:
                video_id = V.split("/")[-2]  # Extract video_id from URL
                url = f"https://madxapi-d0cbf6ac738c.herokuapp.com/{video_id}/master.m3u8?token={token}"
            else:
                url = "https://" + V

            if "visionias" in url:
                async with ClientSession() as session:
                    async with session.get(url, headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Pragma': 'no-cache', 'Referer': 'http://www.visionias.in/', 'Sec-Fetch-Dest': 'iframe', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'cross-site', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Linux; Android 12; RMX2121) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36', 'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"', 'sec-ch-ua-mobile': '?1', 'sec-ch-ua-platform': '"Android"'}) as resp:
                        text = await resp.text()
                        url = re.search(r"(https://.*?playlist.m3u8.*?)\"", text).group(1)

            elif 'videos.classplusapp' in url:
                url = requests.get(f'https://api.classplusapp.com/cams/uploader/video/jw-signed-url?url={url}', headers={'x-access-token': 'eyJhbGciOiJIUzM4NCIsInR5cCI6IkpXVCJ9.eyJpZCI6MTQxMjY4NjA0LCJvcmdJZCI6NzExNTI4LCJvcmdDb2RlIjoidWphbGFmIiwib3JnTmFtZSI6IlNhcnJ0aGlJQVMiLCJuYW1lIjoiU2R2IiwiZW1haWwiOiJ1cC51bmtub3dua2lsbGVyMTEyMkBnbWFpbC5jb20iLCJtb2JpbGUiOiI5MTk4Mzg2MzIxNTQiLCJ0eXBlIjoxLCJpc0RpeSI6dHJ1ZSwiaXNJbnRlcm5hdGlvbmFsIjowLCJkZWZhdWx0TGFuZ3VhZ2UiOiJFTiIsImNvdW50cnlDb2RlIjoiSU4iLCJ0aW1lem9uZSI6IkdNVCs1OjMwIiwiY291bnRyeUlTTyI6IjkxIiwiaXNEaXlTdWJhZG1pbiI6MCwiZmluZ2VycHJpbnRJZCI6ImVmNzVhMzA0Mjg3NmM2ZDNhNWY0OGY0OTQ5MDVjYTU4IiwiaWF0IjoxNzM4NDkxNjc5LCJleHAiOjE3MzkwOTY0Nzl9.K0qwqLD7xIYJVIdQ0ZxRXXzsKudtI7hNCsBz73gfbYt37_abBlVwMvanYpC-R_yZ'}).json()['url']

            name1 = links[i][0].replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "").replace("*", "").replace(".", "").replace("https", "").replace("http", "").strip()
            name = f'{str(count).zfill(3)}) {name1[:60]}'

            if "youtu" in url:
                ytf = f"b[height<={raw_text2}][ext=mp4]/bv[height<={raw_text2}][ext=mp4]+ba[ext=m4a]/b[ext=mp4]"
            else:
                ytf = f"b[height<={raw_text2}]/bv[height<={raw_text2}]+ba/b/bv+ba"

            if "jw-prod" in url:
                cmd = f'yt-dlp -o "{name}.mp4" "{url}"'
            else:
                cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4"'

            try:
                cc = f'**[📽️] Vid_ID:** {str(count).zfill(3)}.** {name1}{MR}.mkv\n**𝔹ᴀᴛᴄʜ** » **{raw_text0}**'
                cc1 = f'**[📁] Pdf_ID:** {str(count).zfill(3)}. {name1}{MR}.pdf \n**𝔹ᴀᴛᴄʜ** » **{raw_text0}**'
                if "drive" in url:
                    try:
                        ka = await helper.download(url, name)
                        copy = await bot.send_document(chat_id=m.chat.id, document=ka, caption=cc1)
                        count += 1
                        os.remove(ka)
                        time.sleep(1)
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue

                elif ".pdf" in url:
                    try:
                        cmd = f'yt-dlp -o "{name}.pdf" "{url}"'
                        download_cmd = f"{cmd} -R 25 --fragment-retries 25"
                        os.system(download_cmd)
                        copy = await bot.send_document(chat_id=m.chat.id, document=f'{name}.pdf', caption=cc1)
                        count += 1
                        os.remove(f'{name}.pdf')
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue
                else:
                    Show = f"**⥥ 🄳🄾🅆🄽🄻🄾🄰🄳🄸🄽🄶⬇️⬇️... »**\n\n**📝Name »** `{name}\n❄Quality » {raw_text2}`\n\n**🔗URL »** `{url}`"
                    prog = await m.reply_text(Show)
                    res_file = await helper.download_video(url, cmd, name)
                    filename = res_file
                    await prog.delete(True)
                    await helper.send_vid(bot, m, cc, filename, thumb, name, prog)
                    count += 1
                    time.sleep(1)

            except Exception as e:
                await m.reply_text(
                    f"**downloading Interupted **\n{str(e)}\n**Name** » {name}\n**Link** » `{url}`"
                )
                continue

    except Exception as e:
        await m.reply_text(f"An error occurred: {str(e)}")
    finally:
        # Remove user from active users
        if user_id in active_users:
            del active_users[user_id]

    await m.reply_text("**𝔻ᴏɴᴇ 𝔹ᴏ𝕤𝕤😎**")

# Background task to clean up inactive users
async def cleanup_active_users():
    while True:
        await asyncio.sleep(300)  # Check every 5 minutes
        current_time = datetime.now()
        inactive_users = [
            uid for uid, user_data in active_users.items()
            if (current_time - user_data['start_time']).total_seconds() > 1800  # 30 minutes
        ]
        
        for uid in inactive_users:
            del active_users[uid]

# Start the cleanup task
bot.loop.create_task(cleanup_active_users())

bot.run()
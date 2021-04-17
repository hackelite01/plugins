# COPYRIGHT  BY mayank1rajput

"""
👻👻👻👻👻👻👻👻👻👻👻👻👻👻@mayank1rajput👻👻👻👻👻👻👻👻👻👻👻👻👻👻
👻👻👻👻👻👻👻👻👻👻👻👻👻👻@mayank1rajput👻👻👻👻👻👻👻👻👻👻👻👻👻👻
👻👻👻👻👻👻👻👻👻👻👻👻👻👻@mayank1rajput👻👻👻👻👻👻👻👻👻👻👻👻👻👻
👻👻👻👻👻👻👻👻👻👻👻👻👻👻@mayank1rajput👻👻👻👻👻👻👻👻👻👻👻👻👻👻
                 MADE BY mayank1rajput
                 PLEASE KEEP CREDITS -_-
"""



from telethon import events, Button, custom
from skull import BOT
import os,re
from telethon.tl.custom import Button 
from telethon import events, errors, custom, functions
@tgbot.on(events.InlineQuery(pattern=r"repo"))
async def inline_id_handler(event: events.InlineQuery.Event):
 skull = event.builder
 馃拃= [[custom.Button.inline( CLICK ME",data="obhai")]]
 query = event.text
 result = skull.article("skull",text="REPO AND SUPPORT",buttons=馃拃,link_preview=False)
 await event.answer([result])
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"ohhh")))
async def callback_query_handler(event):

# inline by mayank1rajput
  await event.edit(text=f"{BOT} REPO AND GROUP LINK",buttons=[[Button.url(f{BOT} REP", url="https://github.com/hackelite01/skull-userbot"), Button.url(f"鈿BOT} SUPPORT鈿�", url="https://t.me/skulluserbot_support")]])
# credits to @mayank1rajput

#  Copyright (C) 2021  mayank
import asyncio
import base64
import os
import re

from telethon.tl.functions.messages import ImportChatInviteRequest as Get

from . import (
    changemymind,
    deEmojify,
    fakegs,
    kannagen,
    moditweet,
    reply_id,
    trumptweet,
    tweets,
)


@bot.on(admin_cmd(outgoing=True, pattern="fakegs(?: |$)(.*)", command="fakegs"))
@bot.on(sudo_cmd(allow_sudo=True, pattern="fakegs(?: |$)(.*)", command="fakegs"))
async def nekobot(marcus):
    if marcus.fwd_from:
        return
    text = marcus.pattern_match.group(1)
    reply_to_id = await reply_id(marcus)
    if not text:
        if marcus.is_reply and not reply_to_id.media:
            text = reply_to_id.message
        else:
            await edit_delete(marcus, "`What should i search in google.`", 5)
            return
    marcuse = await edit_or_reply(marcus, "`Connecting to https://www.google.com/ ...`")
    text = deEmojify(text)
    if ";" in text:
        search, result = text.split(";")
    else:
        await edit_delete(
            marcus,
            "__How should i create meme follow the syntax as show__ `.fakegs top text ; bottom text`",
            5,
        )
        return
    marcusfile = await fakegs(search, result)
    await asyncio.sleep(2)
    await marcus.client.send_file(marcus.chat_id, marcusfile, reply_to=reply_to_id)
    await marcuse.delete()
    if os.path.exists(marcusfile):
        os.remove(marcusfile)


@bot.on(admin_cmd(outgoing=True, pattern="trump(?: |$)(.*)", command="trump"))
@bot.on(sudo_cmd(allow_sudo=True, pattern="trump(?: |$)(.*)", command="trump"))
async def nekobot(marcus):
    if marcus.fwd_from:
        return
    text = marcus.pattern_match.group(1)
    text = re.sub("&", "", text)
    reply_to_id = await reply_id(marcus)
    hmm = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    reply = await marcus.get_reply_message()
    if not text:
        if marcus.is_reply and not reply.media:
            text = reply.message
        else:
            await edit_delete(marcus, "**Trump : **`What should I tweet`", 5)
            return
    marcuse = await edit_or_reply(marcus, "`Requesting trump to tweet...`")
    try:
        hmm = Get(hmm)
        await marcus.client(hmm)
    except BaseException:
        pass
    text = deEmojify(text)
    await asyncio.sleep(2)
    marcusfile = await trumptweet(text)
    await marcus.client.send_file(marcus.chat_id, marcusfile, reply_to=reply_to_id)
    await marcuse.delete()
    if os.path.exists(marcusfile):
        os.remove(marcusfile)


@bot.on(admin_cmd(outgoing=True, pattern="modi(?: |$)(.*)", command="modi"))
@bot.on(sudo_cmd(allow_sudo=True, pattern="modi(?: |$)(.*)", command="modi"))
async def nekobot(marcus):
    if marcus.fwd_from:
        return
    text = marcus.pattern_match.group(1)
    text = re.sub("&", "", text)
    reply_to_id = await reply_id(marcus)
    hmm = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    reply = await marcus.get_reply_message()
    if not text:
        if marcus.is_reply and not reply.media:
            text = reply.message
        else:
            await edit_delete(marcus, "**Modi : **`What should I tweet`", 5)
            return
    marcuse = await edit_or_reply(marcus, "Requesting modi to tweet...")
    try:
        hmm = Get(hmm)
        await marcus.client(hmm)
    except BaseException:
        pass
    text = deEmojify(text)
    await asyncio.sleep(2)
    marcusfile = await moditweet(text)
    await marcus.client.send_file(marcus.chat_id, marcusfile, reply_to=reply_to_id)
    await marcuse.delete()
    if os.path.exists(marcusfile):
        os.remove(marcusfile)


@bot.on(admin_cmd(outgoing=True, pattern="cmm(?: |$)(.*)", command="cmm"))
@bot.on(sudo_cmd(allow_sudo=True, pattern="cmm(?: |$)(.*)", command="cmm"))
async def nekobot(marcus):
    if marcus.fwd_from:
        return
    text = marcus.pattern_match.group(1)
    text = re.sub("&", "", text)
    reply_to_id = await reply_id(marcus)
    hmm = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    reply = await marcus.get_reply_message()
    if not text:
        if marcus.is_reply and not reply.media:
            text = reply.message
        else:
            await edit_delete(marcus, "`Give text to write on banner, man`", 5)
            return
    marcuse = await edit_or_reply(marcus, "`Your banner is under creation wait a sec...`")
    try:
        hmm = Get(hmm)
        await marcus.client(hmm)
    except BaseException:
        pass
    text = deEmojify(text)
    await asyncio.sleep(2)
    marcusfile = await changemymind(text)
    await marcus.client.send_file(marcus.chat_id, marcusfile, reply_to=reply_to_id)
    await marcuse.delete()
    if os.path.exists(catfile):
        os.remove(catfile)


@bot.on(admin_cmd(outgoing=True, pattern="kanna(?: |$)(.*)", command="kanna"))
@bot.on(sudo_cmd(allow_sudo=True, pattern="kanna(?: |$)(.*)", command="kanna"))
async def nekobot(marcus):
    if marcus.fwd_from:
        return
    text = marcus.pattern_match.group(1)
    text = re.sub("&", "", text)
    reply_to_id = await reply_id(marcus)
    hmm = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    reply = await marcus.get_reply_message()
    if not text:
        if marcus.is_reply and not reply.media:
            text = reply.message
        else:
            await edit_delete(marcus, "**Kanna : **`What should i show you`", 5)
            return
    cate = await edit_or_reply(marcus, "`Kanna is writing your text...`")
    try:
        hmm = Get(hmm)
        await e.client(hmm)
    except BaseException:
        pass
    text = deEmojify(text)
    await asyncio.sleep(2)
    catfile = await kannagen(text)
    await marcus.client.send_file(marcus.chat_id, catfile, reply_to=reply_to_id)
    await cate.delete()
    if os.path.exists(catfile):
        os.remove(catfile)


@bot.on(admin_cmd(outgoing=True, pattern="tweet(?: |$)(.*)", command="tweet"))
@bot.on(sudo_cmd(allow_sudo=True, pattern="tweet(?: |$)(.*)", command="tweet"))
async def nekobot(marcus):
    if marcus.fwd_from:
        return
    text = marcus.pattern_match.group(1)
    text = re.sub("&", "", text)
    reply_to_id = await reply_id(marcus)
    hmm = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    reply = await marcus.get_reply_message()
    if not text:
        if marcus.is_reply and not reply.media:
            text = reply.message
        else:
            await edit_delete(
                marcus,
                "what should I tweet? Give some text and format must be like `.tweet username ; your text` ",
                5,
            )
            return
    try:
        hmm = Get(hmm)
        await marcus.client(hmm)
    except BaseException:
        pass
    if ";" in text:
        username, text = text.split(";")
    else:
        await edit_delete(
            marcus,
            "__what should I tweet? Give some text and format must be like__ `.tweet username ; your text`",
            5,
        )
        return
    marcuse = await edit_or_reply(marcus, f"`Requesting {username} to tweet...`")
    text = deEmojify(text)
    await asyncio.sleep(2)
    marcusfile = await tweets(text, username)
    await marcus.client.send_file(marcus.chat_id, marcusfile, reply_to=reply_to_id)
    await marcuse.delete()
    if os.path.exists(marcusfile):
        os.remove(marcusfile)


CMD_HELP.update(
    {
        "imgmemes": """**Plugin : **`imgmemes`

  •  **Syntax : **`.fakegs search query ; what you mean text`
  •  **Function : **__Shows you image meme for your google search query__  

  •  **Syntax : **`.trump reply/text`
  •  **Function : **__sends you the trump tweet sticker with given custom text__

  •  **Syntax : **`.modi reply/text`
  •  **Function : **__sends you the modi tweet sticker with given custom text__ 

  •  **Syntax : **`.cmm reply/text`
  •  **Function : **__sends you the  Change my mind banner with given custom text__ 

  •  **Syntax : **`.kanna reply/text`
  •  **Function : **__sends you the kanna chan sticker with given custom text__  

  •  **Syntax : **`.tweet reply/<username> ; <text>`
  •  **Function : **__sends you the desired person tweet sticker with given custom text__ 
  """
    }
)

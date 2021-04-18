# collage plugin for marcususerbot by @mayank1rajput

# Copyright (C) 2020 Alfiananda P.A
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.

import os

from . import make_gif


@bot.on(admin_cmd(pattern="collage(?: |$)(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="collage(?: |$)(.*)", allow_sudo=True))
async def collage(marcus):
    if marcus.fwd_from:
        return
    marcusinput = marcus.pattern_match.group(1)
    reply = await marcus.get_reply_message()
    marcusid = marcus.reply_to_msg_id
    marcus = await edit_or_reply(
        marcus, "```collaging this may take several minutes too..... 馃榿```"
    )
    if not (reply and (reply.media)):
        await marcus.edit("`Media not found...`")
        return
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    marcussticker = await reply.download_media(file="./temp/")
    if not marcussticker.endswith((".mp4", ".mkv", ".tgs")):
        os.remove(marcussticker)
        await marcus.edit("`Media format is not supported...`")
        return
    if marcusinput:
        if not marcusinput.isdigit():
            os.remove(marcussticker)
            await marcus.edit("`You input is invalid, check help`")
            return
        marcusinput = int(marcusinput)
        if not 0 < marcusinput < 10:
            os.remove(marcussticker)
            await marcus.edit(
                "`Why too big grid you cant see images, use size of grid between 1 to 9`"
            )
            return
    else:
        marcusinput = 3
    if marcussticker.endswith(".tgs"):
        hmm = await make_gif(marcus, marcussticker)
        if hmm.endswith(("@tgstogifbot")):
            os.remove(marcussticker)
            return await marcus.edit(hmm)
        collagefile = hmm
    else:
        collagefile = marcussticker
    endfile = "./temp/collage.png"
    marcuscmd = f"vcsi -g {marcusinput}x{marcusinput} '{collagefile}' -o {endfile}"
    stdout, stderr = (await _marcusutils.runcmd(marcuscmd))[:2]
    if not os.path.exists(endfile):
        for files in (marcussticker, collagefile):
            if files and os.path.exists(files):
                os.remove(files)
        return await edit_delete(
            marcus, f"`media is not supported or try with smaller grid size`", 5
        )
    await marcus.client.send_file(
        marcus.chat_id,
        endfile,
        reply_to=marcusid,
    )
    await marcus.delete()
    for files in (marcussticker, collagefile, endfile):
        if files and os.path.exists(files):
            os.remove(files)


CMD_HELP.update(
    {
        "collage": "**Plugin : **`collage`\
        \n\n  鈥�  **Syntax : **`.collage <grid size>`\
        \n  鈥�  **Function : **__Shows you the grid image of images extracted from video \n Grid size must be between 1 to 9 by default it is 3__"
    }
)

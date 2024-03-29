import asyncio
import os
import subprocess
import time
from datetime import datetime
from pathlib import Path
from shutil import copyfile

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from pymediainfo import MediaInfo
from telethon.tl.types import DocumentAttributeVideo

from . import make_gif, progress, reply_id, thumb_from_audio

PATH = os.path.join("./temp", "temp_vid.mp4")
thumb_image_path = os.path.join(Config.TMP_DOWNLOAD_DIRECTORY, "thumb_image.jpg")


class UPLOAD:
    def __init__(self):
        self.uploaded = 0


UPLOAD_ = UPLOAD()


async def marcuslst_of_files(path):
    files = []
    for dirname, dirnames, filenames in os.walk(path):
        # print path to all filenames.
        for filename in filenames:
            files.append(os.path.join(dirname, filename))
    return files


def get_video_thumb(file, output=None, width=320):
    output = file + ".jpg"
    metadata = extractMetadata(createParser(file))
    cmd = [
        "ffmpeg",
        "-i",
        file,
        "-ss",
        str(int((0, metadata.get("duration").seconds)[metadata.has("duration")] / 2)),
        # '-filter:v', 'scale={}:-1'.format(width),
        "-vframes",
        "1",
        output,
    ]
    p = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    p.communicate()
    if not p.returncode and os.path.lexists(file):
        return output


def sortthings(contents, path):
    marcussort = []
    contents.sort()
    for file in contents:
        marcuspath = os.path.join(path, file)
        if os.path.isfile(marcuspath):
            marcussort.append(file)
    for file in contents:
        marcuspath = os.path.join(path, file)
        if os.path.isdir(marcuspath):
            marcussort.append(file)
    return marcussort


async def upload(path, event, udir_event, marcusflag=None):
    marcusflag = marcusflag or False
    reply_to_id = await reply_id(event)
    if os.path.isdir(path):
        await event.client.send_message(
            event.chat_id,
            f"**Folder : **`{str(path)}`",
        )
        Files = os.listdir(path)
        Files = sortthings(Files, path)
        for file in Files:
            marcuspath = os.path.join(path, file)
            await upload(marcuspath, event, udir_event)
    elif os.path.isfile(path):
        caption_rts = os.path.basename(path)
        c_time = time.time()
        thumb = None
        if os.path.exists(thumb_image_path):
            thumb = thumb_image_path
        if not caption_rts.lower().endswith(".mp4"):
            await event.client.send_file(
                event.chat_id,
                path,
                caption=f"**File Name : **`{caption_rts}`",
                force_document=marcusflag,
                thumb=thumb,
                reply_to=reply_to_id,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, udir_event, c_time, "Uploading...", caption_rts)
                ),
            )
        else:
            metadata = extractMetadata(createParser(str(path)))
            duration = 0
            width = 0
            height = 0
            if metadata.has("duration"):
                duration = metadata.get("duration").seconds
            if metadata.has("width"):
                width = metadata.get("width")
            if metadata.has("height"):
                height = metadata.get("height")
            await event.client.send_file(
                event.chat_id,
                path,
                caption=f"**File Name : **`{caption_rts}`",
                thumb=thumb,
                force_document=marcusflag,
                reply_to=reply_to_id,
                supports_streaming=True,
                attributes=[
                    DocumentAttributeVideo(
                        duration=duration,
                        w=width,
                        h=height,
                        round_message=False,
                        supports_streaming=True,
                    )
                ],
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, udir_event, c_time, "Uploading...", caption_rts)
                ),
            )
        UPLOAD_.uploaded += 1


@bot.on(admin_cmd(pattern="upload (.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="upload (.*)", allow_sudo=True))
async def uploadir(event):
    input_str = "".join(event.text.split(maxsplit=1)[1:])
    path = Path(input_str)
    start = datetime.now()
    if not os.path.exists(path):
        await edit_or_reply(
            event,
            f"`there is no such directory/file with the name {path} to upload`",
        )
        return
    udir_event = await edit_or_reply(event, "Uploading....")
    if os.path.isdir(path):
        await edit_or_reply(udir_event, f"`Gathering file details in directory {path}`")
        UPLOAD_.uploaded = 0
        await upload(path, event, udir_event)
        end = datetime.now()
        ms = (end - start).seconds
        await udir_event.edit(
            f"`Uploaded {UPLOAD_.uploaded} files successfully in {ms} seconds. `"
        )
    else:
        await edit_or_reply(udir_event, f"`Uploading.....`")
        UPLOAD_.uploaded = 0
        await upload(path, event, udir_event)
        end = datetime.now()
        ms = (end - start).seconds
        await udir_event.edit(
            f"`Uploaded file {str(path)} successfully in {ms} seconds. `"
        )
    await asyncio.sleep(5)
    await udir_event.delete()


@bot.on(admin_cmd(pattern="uploadf (.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="uploadf (.*)", allow_sudo=True))
async def uploadir(event):
    input_str = "".join(event.text.split(maxsplit=1)[1:])
    path = Path(input_str)
    start = datetime.now()
    if not os.path.exists(path):
        await edit_or_reply(
            event,
            f"`there is no such directory/file with the name {path} to upload`",
        )
        return
    udir_event = await edit_or_reply(event, "Uploading....")
    if os.path.isdir(path):
        await edit_or_reply(udir_event, f"`Gathering file details in directory {path}`")
        UPLOAD_.uploaded = 0
        await upload(path, event, udir_event, marcusflag=True)
        end = datetime.now()
        ms = (end - start).seconds
        await udir_event.edit(
            f"`Uploaded {UPLOAD_.uploaded} files successfully in {ms} seconds. `"
        )
    else:
        await edit_or_reply(udir_event, f"`Uploading.....`")
        UPLOAD_.uploaded = 0
        await upload(path, event, udir_event, marcusflag=True)
        end = datetime.now()
        ms = (end - start).seconds
        await udir_event.edit(
            f"`Uploaded file {str(path)} successfully in {ms} seconds. `"
        )
    await asyncio.sleep(5)
    await udir_event.delete()


@bot.on(admin_cmd(pattern="circle ?(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="circle ?(.*)", allow_sudo=True))
async def video_marcusfile(event):
    reply = await event.get_reply_message()
    input_str = "".join(event.text.split(maxsplit=1)[1:])
    if input_str:
        path = Path(input_str)
        if not os.path.exists(path):
            await edit_or_reply(
                event,
                f"`there is no such directory/file with the name {path} to upload`",
            )
            return
        marcusevent = await edit_or_reply(event, "`Converting to video note..........`")
        filename = os.path.basename(path)
        marcusfile = os.path.join("./temp", filename)
        copyfile(path, marcusfile)
    else:
        if not reply:
            await edit_delete(event, "`Reply to supported media`", 5)
            return
        if not (reply and (reply.media)):
            await edit_delete(event, "`Reply to supported Media...`", 5)
            return
        marcusevent = await edit_or_reply(event, "`Converting to video note..........`")
        marcusfile = await reply.download_media(file="./temp/")
    if not marcusfile.endswith((".mp4", ".tgs", ".mp3", ".mov", ".gif", ".opus")):
        os.remove(marcusfile)
        await edit_delete(marcusevent, "```Supported Media not found...```", 5)
        return
    if marcusfile.endswith((".mp4", ".tgs", ".mov", ".gif")):
        if marcusfile.endswith((".tgs")):
            hmm = await make_gif(marcusevent, marcusfile)
            if hmm.endswith(("@tgstogifbot")):
                os.remove(marcusfile)
                return await marcusevent.edit(hmm)
            os.rename(hmm, "./temp/circle.mp4")
            marcusfile = "./temp/circle.mp4"
        media_info = MediaInfo.parse(marcusfile)
        aspect_ratio = 1
        for track in media_info.tracks:
            if track.track_type == "Video":
                aspect_ratio = track.display_aspect_ratio
                height = track.height
                width = track.width
        if aspect_ratio != 1:
            crop_by = width if (height > width) else height
            await _marcusutils.runcmd(
                f'ffmpeg -i {marcusfile} -vf "crop={crop_by}:{crop_by}" {PATH}'
            )
        else:
            copyfile(marcusfile, PATH)
        if str(marcusfile) != str(PATH):
            os.remove(marcusfile)
    else:
        thumb_loc = os.path.join(Config.TMP_DOWNLOAD_DIRECTORY, "thumb_image.jpg")
        marcusthumb = None
        try:
            marcusthumb = await reply.download_media(thumb=-1)
        except Exception:
            marcusthumb = os.path.join("./temp", "thumb.jpg")
            await thumb_from_audio(marcusfile, marcusthumb)
        if marcusthumb is None:
            marcusthumb = os.path.join("./temp", "thumb.jpg")
            copyfile(thumb_loc, marcusthumb)
        if (
            marcusthumb is not None
            and not os.path.exists(marcusthumb)
            and os.path.exists(thumb_loc)
        ):
            marcusthumb = os.path.join("./temp", "thumb.jpg")
            copyfile(thumb_loc, marcusthumb)
        if marcusthumb is not None and os.path.exists(marcusthumb):
            await _marcusutils.runcmd(
                f"ffmpeg -loop 1 -i {marcusthumb} -i {marcusfile} -c:v libx264 -tune stillimage -c:a aac -b:a 192k -vf \"scale='iw-mod (iw,2)':'ih-mod(ih,2)',format=yuv420p\" -shortest -movflags +faststart {PATH}"
            )
            os.remove(marcusfile)
        else:
            os.remove(marcusfile)
            return await edit_delete(
                marcusevent, "`No thumb found to make it video note`", 5
            )
    if os.path.exists(PATH):
        marcusid = event.reply_to_msg_id
        c_time = time.time()
        await event.client.send_file(
            event.chat_id,
            PATH,
            allow_cache=False,
            reply_to=marcusid,
            video_note=True,
            attributes=[
                DocumentAttributeVideo(
                    duration=60,
                    w=1,
                    h=1,
                    round_message=True,
                    supports_streaming=True,
                )
            ],
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, marcusevent, c_time, "Uploading...", PATH)
            ),
        )
        os.remove(PATH)
    await marcusevent.delete()


CMD_HELP.update(
    {
        "upload": "**Plugin :** `upload`\
    \n\n  •  **Syntax :** `.upload path of file/folder`\
    \n  •  **Function : **__Uploads the file from the server or list of files from that folder as steamable__\
    \n\n  •  **Syntax :** `.uploadf path of file/folder`\
    \n  •  **Function : **__Uploads the file from the server or list of files from that folder as a file__\
    \n\n  •  **Syntax : **`.circle reply to media or path of media`\
    \n  •  **Function : **__Uploads video/audio as streamable from the server__"
    }
)

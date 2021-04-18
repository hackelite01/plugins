"""
idea from lynda and rose bot
made by @mayank1rajput
"""
from telethon.errors import BadRequestError
from telethon.errors.rpcerrorlist import UserAdminInvalidError, UserIdInvalidError
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights

from ..utils import errors_handler
from . import BOTLOG, BOTLOG_CHATID, extract_time, get_user_from_event

# =================== CONSTANT ===================
NO_ADMIN = "`I am not an admin nub nibba!`"
NO_PERM = "`I don't have sufficient permissions! This is so sed. Alexa play despacito`"


@bot.on(admin_cmd(pattern=r"tmute(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern=r"tmute(?: |$)(.*)", allow_sudo=True))
@errors_handler
async def tmuter(marcusy):
    chat = await marcusy.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    # If not admin and not creator, return
    if not admin and not creator:
        await edit_or_reply(marcusy, NO_ADMIN)
        return
    marcusevent = await edit_or_reply(marcusy, "`muting....`")
    user, reason = await get_user_from_event(marcusy, marcusevent)
    if not user:
        return
    if reason:
        reason = reason.split(" ", 1)
        hmm = len(reason)
        marcustime = reason[0]
        reason = reason[1] if hmm == 2 else None
    else:
        await marcusevent.edit("you haven't mentioned time, check `.info tadmin`")
        return
    self_user = await marcusy.client.get_me()
    ctime = await extract_time(marcusy, marcustime)
    if not ctime:
        await marcusevent.edit(
            f"Invalid time type specified. Expected m , h , d or w not as {marcustime}"
        )
        return
    if user.id == self_user.id:
        await marcusevent.edit(f"Sorry, I can't mute myself")
        return
    try:
        await marcusevent.client(
            EditBannedRequest(
                marcusy.chat_id,
                user.id,
                ChatBannedRights(until_date=ctime, send_messages=True),
            )
        )
        # Announce that the function is done
        if reason:
            await marcusevent.edit(
                f"{_format.mentionuser(user.first_name ,user.id)} was muted in {marcusy.chat.title}\n"
                f"**Muted for : **{marcustime}\n"
                f"**Reason : **__{reason}__"
            )
            if BOTLOG:
                await marcusy.client.send_message(
                    BOTLOG_CHATID,
                    "#TMUTE\n"
                    f"**User : **[{user.first_name}](tg://user?id={user.id})\n"
                    f"**Chat : **{marcusy.chat.title}(`{marcusy.chat_id}`)\n"
                    f"**Muted for : **`{marcustime}`\n"
                    f"**Reason : **`{reason}``",
                )
        else:
            await marcusevent.edit(
                f"{_format.mentionuser(user.first_name ,user.id)} was muted in {marcusy.chat.title}\n"
                f"Muted for {marcustime}\n"
            )
            if BOTLOG:
                await marcusy.client.send_message(
                    BOTLOG_CHATID,
                    "#TMUTE\n"
                    f"**User : **[{user.first_name}](tg://user?id={user.id})\n"
                    f"**Chat : **{marcusy.chat.title}(`{marcusy.chat_id}`)\n"
                    f"**Muted for : **`{marcustime}`",
                )
        # Announce to logging group
    except UserIdInvalidError:
        return await marcusevent.edit("`Uh oh my mute logic broke!`")
    except UserAdminInvalidError:
        return await marcusevent.edit(
            "`Either you're not an admin or you tried to mute an admin that you didn't promote`"
        )
    except Exception as e:
        return await marcusevent.edit(f"`{str(e)}`")


@bot.on(admin_cmd(pattern="tban(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern="tban(?: |$)(.*)", allow_sudo=True))
@errors_handler
async def ban(marcusy):
    chat = await marcusy.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    # If not admin and not creator, return
    if not admin and not creator:
        await edit_or_reply(marcusy, NO_ADMIN)
        return
    marcusevent = await edit_or_reply(marcusy, "`banning....`")
    user, reason = await get_user_from_event(marcusy, marcusevent)
    if not user:
        return
    if reason:
        reason = reason.split(" ", 1)
        hmm = len(reason)
        marcustime = reason[0]
        reason = reason[1] if hmm == 2 else None
    else:
        await marcusevent.edit("you haven't mentioned time, check `.info tadmin`")
        return
    self_user = await marcusy.client.get_me()
    ctime = await extract_time(marcusy, marcustime)
    if not ctime:
        await marcusevent.edit(
            f"Invalid time type specified. Expected m , h , d or w not as {marcustime}"
        )
        return
    if user.id == self_user.id:
        await marcusevent.edit(f"Sorry, I can't ban myself")
        return
    await marcusevent.edit("`Whacking the pest!`")
    try:
        await marcusy.client(
            EditBannedRequest(
                marcusy.chat_id,
                user.id,
                ChatBannedRights(until_date=ctime, view_messages=True),
            )
        )
    except UserAdminInvalidError:
        return await marcusevent.edit(
            "`Either you're not an admin or you tried to ban an admin that you didn't promote`"
        )
    except BadRequestError:
        await marcusevent.edit(NO_PERM)
        return
    # Helps ban group join spammers more easily
    try:
        reply = await marcusy.get_reply_message()
        if reply:
            await reply.delete()
    except BadRequestError:
        await marcusevent.edit(
            "`I dont have message nuking rights! But still he was banned!`"
        )
        return
    # Delete message and then tell that the command
    # is done gracefully
    # Shout out the ID, so that fedadmins can fban later
    if reason:
        await marcusevent.edit(
            f"{_format.mentionuser(user.first_name ,user.id)} was banned in {marcusy.chat.title}\n"
            f"banned for {marcustime}\n"
            f"Reason:`{reason}`"
        )
        if BOTLOG:
            await marcusy.client.send_message(
                BOTLOG_CHATID,
                "#TBAN\n"
                f"**User : **[{user.first_name}](tg://user?id={user.id})\n"
                f"**Chat : **{marcusy.chat.title}(`{marcusy.chat_id}`)\n"
                f"**Banned untill : **`{marcustime}`\n"
                f"**Reason : **__{reason}__",
            )
    else:
        await marcusevent.edit(
            f"{_format.mentionuser(user.first_name ,user.id)} was banned in {marcusy.chat.title}\n"
            f"banned for {marcustime}\n"
        )
        if BOTLOG:
            await marcusy.client.send_message(
                BOTLOG_CHATID,
                "#TBAN\n"
                f"**User : **[{user.first_name}](tg://user?id={user.id})\n"
                f"**Chat : **{marcusy.chat.title}(`{marcusy.chat_id}`)\n"
                f"**Banned untill : **`{marcustime}`",
            )


CMD_HELP.update(
    {
        "tadmin": "**Plugin :** `tadmin`\
      \n\n•  **Syntax : **`.tmute <reply/username/userid> <time> <reason>`\
      \n•  **Function : **__Temporary mutes the user for given time.__\
      \n\n•  **Syntax : **`.tban <reply/username/userid> <time> <reason>`\
      \n•  **Function : **__Temporary bans the user for given time.__\
      \n\n•  **Time units : ** __(2m = 2 minutes) ,(3h = 3hours)  ,(4d = 4 days) ,(5w = 5 weeks)\
      These times are example u can use anything with those units __"
    }
)

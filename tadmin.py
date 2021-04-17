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
async def tmuter(skully):
    chat = await skully.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    # If not admin and not creator, return
    if not admin and not creator:
        await edit_or_reply(skully, NO_ADMIN)
        return
    skullevent = await edit_or_reply(skully, "`muting....`")
    user, reason = await get_user_from_event(skully, skullevent)
    if not user:
        return
    if reason:
        reason = reason.split(" ", 1)
        hmm = len(reason)
        skulltime = reason[0]
        reason = reason[1] if hmm == 2 else None
    else:
        await skullevent.edit("you haven't mentioned time, check `.info tadmin`")
        return
    self_user = await skully.client.get_me()
    ctime = await extract_time(skully, skulltime)
    if not ctime:
        await skullevent.edit(
            f"Invalid time type specified. Expected m , h , d or w not as {skulltime}"
        )
        return
    if user.id == self_user.id:
        await skullevent.edit(f"Sorry, I can't mute myself")
        return
    try:
        await skullevent.client(
            EditBannedRequest(
                skully.chat_id,
                user.id,
                ChatBannedRights(until_date=ctime, send_messages=True),
            )
        )
        # Announce that the function is done
        if reason:
            await skullevent.edit(
                f"{_format.mentionuser(user.first_name ,user.id)} was muted in {skully.chat.title}\n"
                f"**Muted for : **{skulltime}\n"
                f"**Reason : **__{reason}__"
            )
            if BOTLOG:
                await skully.client.send_message(
                    BOTLOG_CHATID,
                    "#TMUTE\n"
                    f"**User : **[{user.first_name}](tg://user?id={user.id})\n"
                    f"**Chat : **{skully.chat.title}(`{skully.chat_id}`)\n"
                    f"**Muted for : **`{skulltime}`\n"
                    f"**Reason : **`{reason}``",
                )
        else:
            await skullevent.edit(
                f"{_format.mentionuser(user.first_name ,user.id)} was muted in {skully.chat.title}\n"
                f"Muted for {skulltime}\n"
            )
            if BOTLOG:
                await skully.client.send_message(
                    BOTLOG_CHATID,
                    "#TMUTE\n"
                    f"**User : **[{user.first_name}](tg://user?id={user.id})\n"
                    f"**Chat : **{skully.chat.title}(`{skully.chat_id}`)\n"
                    f"**Muted for : **`{skulltime}`",
                )
        # Announce to logging group
    except UserIdInvalidError:
        return await skullevent.edit("`Uh oh my mute logic broke!`")
    except UserAdminInvalidError:
        return await skullevent.edit(
            "`Either you're not an admin or you tried to mute an admin that you didn't promote`"
        )
    except Exception as e:
        return await skullevent.edit(f"`{str(e)}`")


@bot.on(admin_cmd(pattern="tban(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern="tban(?: |$)(.*)", allow_sudo=True))
@errors_handler
async def ban(skully):
    chat = await skully.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    # If not admin and not creator, return
    if not admin and not creator:
        await edit_or_reply(skully, NO_ADMIN)
        return
    skullevent = await edit_or_reply(skully, "`banning....`")
    user, reason = await get_user_from_event(skully, skullevent)
    if not user:
        return
    if reason:
        reason = reason.split(" ", 1)
        hmm = len(reason)
        skulltime = reason[0]
        reason = reason[1] if hmm == 2 else None
    else:
        await skullevent.edit("you haven't mentioned time, check `.info tadmin`")
        return
    self_user = await skully.client.get_me()
    ctime = await extract_time(skully, skulltime)
    if not ctime:
        await skullevent.edit(
            f"Invalid time type specified. Expected m , h , d or w not as {skulltime}"
        )
        return
    if user.id == self_user.id:
        await skullevent.edit(f"Sorry, I can't ban myself")
        return
    await skullevent.edit("`Whacking the pest!`")
    try:
        await skully.client(
            EditBannedRequest(
                skully.chat_id,
                user.id,
                ChatBannedRights(until_date=ctime, view_messages=True),
            )
        )
    except UserAdminInvalidError:
        return await skullevent.edit(
            "`Either you're not an admin or you tried to ban an admin that you didn't promote`"
        )
    except BadRequestError:
        await skullevent.edit(NO_PERM)
        return
    # Helps ban group join spammers more easily
    try:
        reply = await skully.get_reply_message()
        if reply:
            await reply.delete()
    except BadRequestError:
        await skullevent.edit(
            "`I dont have message nuking rights! But still he was banned!`"
        )
        return
    # Delete message and then tell that the command
    # is done gracefully
    # Shout out the ID, so that fedadmins can fban later
    if reason:
        await skullevent.edit(
            f"{_format.mentionuser(user.first_name ,user.id)} was banned in {skully.chat.title}\n"
            f"banned for {skulltime}\n"
            f"Reason:`{reason}`"
        )
        if BOTLOG:
            await skully.client.send_message(
                BOTLOG_CHATID,
                "#TBAN\n"
                f"**User : **[{user.first_name}](tg://user?id={user.id})\n"
                f"**Chat : **{skully.chat.title}(`{skully.chat_id}`)\n"
                f"**Banned untill : **`{skulltime}`\n"
                f"**Reason : **__{reason}__",
            )
    else:
        await skullevent.edit(
            f"{_format.mentionuser(user.first_name ,user.id)} was banned in {skully.chat.title}\n"
            f"banned for {skulltime}\n"
        )
        if BOTLOG:
            await skully.client.send_message(
                BOTLOG_CHATID,
                "#TBAN\n"
                f"**User : **[{user.first_name}](tg://user?id={user.id})\n"
                f"**Chat : **{skully.chat.title}(`{skully.chat_id}`)\n"
                f"**Banned untill : **`{skulltime}`",
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

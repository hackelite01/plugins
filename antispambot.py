#    Copyright (C) 2021 mayank
# baning spmmers plugin for marcususerbot by @mayank1rajput
# included both cas(combot antispam service) and spamwatch (need to add more feaututres)

from requests import get
from telethon import events
from telethon.errors import ChatAdminRequiredError
from telethon.tl.types import ChannelParticipantsAdmins

from ..utils import is_admin
from . import BOTLOG, BOTLOG_CHATID, LOGS, spamwatch
from .sql_helper.gban_sql_helper import get_gbanuser, is_gbanned

if Config.ANTISPAMBOT_BAN:

    @bot.on(events.ChatAction())
    async def anti_spambot(event):
        if not event.user_joined and not event.user_added:
            return
        chat = event.chat_id
        user = await event.get_user()
        marcusadmin = await is_admin(bot, chat, bot.uid)
        if not marcusadmin:
            return
        marcusbanned = None
        adder = None
        ignore = None
        if event.user_added:
            try:
                adder = event.action_message.sender_id
            except AttributeError:
                return
        async for admin in event.client.iter_participants(
            event.chat_id, filter=ChannelParticipantsAdmins
        ):
            if admin.id == adder:
                ignore = True
                break
        if ignore:
            return
        if is_gbanned(user.id):
            marcusgban = get_gbanuser(user.id)
            if marcusgban.reason:
                hmm = await event.reply(
                    f"[{user.first_name}](tg://user?id={user.id}) was gbanned by you for the reason `{marcusgban.reason}`"
                )
            else:
                hmm = await event.reply(
                    f"[{user.first_name}](tg://user?id={user.id}) was gbanned by you"
                )
            try:
                await bot.edit_permissions(chat, user.id, view_messages=False)
                marcusbanned = True
            except Exception as e:
                LOGS.info(e)
        if spamwatch and not marcusbanned:
            ban = spamwatch.get_ban(user.id)
            if ban:
                hmm = await event.reply(
                    f"[{user.first_name}](tg://user?id={user.id}) was banned by spamwatch for the reason `{ban.reason}`"
                )
                try:
                    await bot.edit_permissions(chat, user.id, view_messages=False)
                    marcusbanned = True
                except Exception as e:
                    LOGS.info(e)
        if not marcusbanned:
            try:
                casurl = "https://api.cas.chat/check?user_id={}".format(user.id)
                data = get(casurl).json()
            except Exception as e:
                LOGS.info(e)
                data = None
            if data and data["ok"]:
                reason = (
                    f"[Banned by Combot Anti Spam](https://cas.chat/query?u={user.id})"
                )
                hmm = await event.reply(
                    f"[{user.first_name}](tg://user?id={user.id}) was banned by Combat anti-spam service(CAS) for the reason check {reason}"
                )
                try:
                    await bot.edit_permissions(chat, user.id, view_messages=False)
                    marcusbanned = True
                except Exception as e:
                    LOGS.info(e)
        if BOTLOG and marcusbanned:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#ANTISPAMBOT\n"
                f"**User :** [{user.first_name}](tg://user?id={user.id})\n"
                f"**Chat :** {event.chat.title} (`{event.chat_id}`)\n"
                f"**Reason :** {hmm.text}",
            )


@bot.on(admin_cmd(pattern="cascheck$"))
@bot.on(sudo_cmd(pattern="cascheck$", allow_sudo=True))
async def caschecker(cas):
    marcusevent = await edit_or_reply(
        cas,
        "`checking any cas(combot antispam service) banned users here, this may take several minutes too......`",
    )
    text = ""
    chat = cas.chat_id
    try:
        info = await cas.client.get_entity(chat)
    except (TypeError, ValueError) as err:
        await cas.edit(str(err))
        return
    try:
        cas_count, members_count = (0,) * 2
        banned_users = ""
        async for user in cas.client.iter_participants(info.id):
            if banchecker(user.id):
                cas_count += 1
                if not user.deleted:
                    banned_users += f"{user.first_name}-`{user.id}`\n"
                else:
                    banned_users += f"Deleted Account `{user.id}`\n"
            members_count += 1
        text = "**Warning!** Found `{}` of `{}` users are CAS Banned:\n".format(
            cas_count, members_count
        )
        text += banned_users
        if not cas_count:
            text = "No CAS Banned users found!"
    except ChatAdminRequiredError as carerr:
        await marcusevent.edit("`CAS check failed: Admin privileges are required`")
        return
    except BaseException as be:
        await marcusevent.edit("`CAS check failed`")
        return
    await marcusevent.edit(text)


@bot.on(admin_cmd(pattern="spamcheck$"))
@bot.on(sudo_cmd(pattern="spamcheck$", allow_sudo=True))
async def caschecker(cas):
    text = ""
    chat = cas.chat_id
    marcusevent = await edit_or_reply(
        cas,
        "`checking any spamwatch banned users here, this may take several minutes too......`",
    )
    try:
        info = await cas.client.get_entity(chat)
    except (TypeError, ValueError) as err:
        await cas.edit(str(err))
        return
    try:
        cas_count, members_count = (0,) * 2
        banned_users = ""
        async for user in cas.client.iter_participants(info.id):
            if spamchecker(user.id):
                cas_count += 1
                if not user.deleted:
                    banned_users += f"{user.first_name}-`{user.id}`\n"
                else:
                    banned_users += f"Deleted Account `{user.id}`\n"
            members_count += 1
        text = "**Warning! **Found `{}` of `{}` users are spamwatch Banned:\n".format(
            cas_count, members_count
        )
        text += banned_users
        if not cas_count:
            text = "No spamwatch Banned users found!"
    except ChatAdminRequiredError as carerr:
        await marcusevent.edit("`spamwatch check failed: Admin privileges are required`")
        return
    except BaseException as be:
        await marcusevent.edit("`spamwatch check failed`")
        return
    await marcusevent.edit(text)


def banchecker(user_id):
    try:
        casurl = "https://api.cas.chat/check?user_id={}".format(user_id)
        data = get(casurl).json()
    except Exception as e:
        LOGS.info(e)
        data = None
    return bool(data and data["ok"])


def spamchecker(user_id):
    ban = None
    if spamwatch:
        ban = spamwatch.get_ban(user_id)
    return bool(ban)


CMD_HELP.update(
    {
        "antispambot": "**Plugin : **`antispambot`\
        \n\n**Syntax : **`.cascheck`\
        \n**Function : **__Searches for cas(combot antispam service) banned users in group and shows you the list__\
        \n\n**Syntax : **`.spamcheck`\
        \n**Function : **__Searches for spamwatch banned users in group and shows you the list__"
    }
)

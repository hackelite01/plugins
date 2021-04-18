import nekos


@bot.on(admin_cmd(pattern="tmarcus$"))
@bot.on(sudo_cmd(pattern="tmarcus$", allow_sudo=True))
async def hmm(marcus):
    if marcus.fwd_from:
        return
    reactmarcus = nekos.textmarcus()
    await edit_or_reply(marcus, reactmarcus)


@bot.on(admin_cmd(pattern="why$"))
@bot.on(sudo_cmd(pattern="why$", allow_sudo=True))
async def hmm(marcus):
    if marcus.fwd_from:
        return
    whymarcus = nekos.why()
    await edit_or_reply(marcus, whymarcus)


@bot.on(admin_cmd(pattern="fact$"))
@bot.on(sudo_cmd(pattern="fact$", allow_sudo=True))
async def hmm(marcus):
    if marcus.fwd_from:
        return
    factmarcus = nekos.fact()
    await edit_or_reply(marcus, factmarcus)


CMD_HELP.update(
    {
        "funtxts": """**Plugin : **`funtxts`

  •  **Syntax : **`.tmarcus`
  •  **Function : **__Sens you some random marcus facial text art__

  •  **Syntax : **`.why`
  •  **Function : **__Asks some random Funny questions__

  •  **Syntax : **`.fact`
  •  **Function : **__Sends you some random facts__"""
    }
)

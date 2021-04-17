# corona virus stats for skulluserbot
from covid import Covid

from . import covidindia


@bot.on(admin_cmd(pattern="covid(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern="covid(?: |$)(.*)", allow_sudo=True))
async def corona(event):
    if event.pattern_match.group(1):
        country = (event.pattern_match.group(1)).title()
    else:
        country = "World"
    skullevent = await edit_or_reply(event, "`Collecting data...`")
    covid = Covid(source="worldometers")
    try:
        country_data = covid.get_status_by_country_name(country)
    except ValueError:
        country_data = ""
    if country_data:
        hmm1 = country_data["confirmed"] + country_data["new_cases"]
        hmm2 = country_data["deaths"] + country_data["new_deaths"]
        data = ""
        data += f"\n鈿狅笍 Confirmed   : <code>{hmm1}</code>"
        data += f"\n馃様 Active           : <code>{country_data['active']}</code>"
        data += f"\n鈿帮笍 Deaths         : <code>{hmm2}</code>"
        data += f"\n馃 Critical          : <code>{country_data['critical']}</code>"
        data += f"\n馃槉 Recovered   : <code>{country_data['recovered']}</code>"
        data += f"\n馃拤 Total tests    : <code>{country_data['total_tests']}</code>"
        data += f"\n馃ズ New Cases   : <code>{country_data['new_cases']}</code>"
        data += f"\n馃槦 New Deaths : <code>{country_data['new_deaths']}</code>"
        await skullevent.edit(
            "<b>Corona Virus Info of {}:\n{}</b>".format(country, data),
            parse_mode="html",
        )
    else:
        data = await covidindia(country)
        if data:
            skull1 = int(data["new_positive"]) - int(data["positive"])
            skull2 = int(data["new_death"]) - int(data["death"])
            skull3 = int(data["new_cured"]) - int(data["cured"])
            result = f"<b>Corona virus info of {data['state_name']}\
                \n\n鈿狅笍 Confirmed   : <code>{data['new_positive']}</code>\
                \n馃様 Active           : <code>{data['new_active']}</code>\
                \n鈿帮笍 Deaths         : <code>{data['new_death']}</code>\
                \n馃槉 Recovered   : <code>{data['new_cured']}</code>\
                \n馃ズ New Cases   : <code>{skull1}</code>\
                \n馃槦 New Deaths : <code>{skull2}</code>\
                \n馃槂 New cured  : <code>{skull3}</code> </b>"
            await skullevent.edit(result, parse_mode="html")
        else:
            await edit_delete(
                skullevent,
                "`Corona Virus Info of {} is not avaiable or unable to fetch`".format(
                    country
                ),
                5,
            )


CMD_HELP.update(
    {
        "covid": "**Plugin : **`covid`\
        \n\n  鈥�  **Syntax : **`.covid <country name>`\
        \n  鈥�  **Function :** __Get an information about covid-19 data in the given country.__\
        \n\n  鈥�  **Syntax : **`.covid <state name>`\
        \n  鈥�  **Function :** __Get an information about covid-19 data in the given state of India only.__\
        "
    }
)

# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

import re
import urllib
import urllib.parse

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from main_start.core.decorators import speedo_on_cmd
from main_start.helper_func.basic_helpers import edit_or_reply, get_text


@speedo_on_cmd(
    ["duckduckgo", "ddg"],
    cmd_help={"help": "duckduckgo searcher!", "example": "{ch}ddg (query to search)"},
)
async def duckduckgo(client, message):
    engine = message.Engine
    pablo = await edit_or_reply(message, engine.get_string("PROCESSING"))
    query = get_text(message)
    if not query:
        await pablo.edit(engine.get_string("INPUT_REQ").format("query"))
        return
    sample_url = "https://duckduckgo.com/?q={}".format(query.replace(" ", "+"))
    link = sample_url.rstrip()
    await pablo.edit(
        engine.get_string("DUCK_DUCK_GO").format(query, link)
    )


@speedo_on_cmd(
    ["gs", "grs", "google"],
    cmd_help={"help": "Google Searcher!", "example": "{ch}gs (query to search)"},
)
async def grs(client, message):
    engine = message.Engine
    pablo = await edit_or_reply(message, engine.get_string("PROCESSING"))
    query = get_text(message)
    if not query:
        await pablo.edit(engine.get_string("INPUT_REQ").format("query"))
        return
    query = urllib.parse.quote_plus(query)
    number_result = 8
    ua = UserAgent()
    google_url = (
        "https://www.google.com/search?q=" + query + "&num=" + str(number_result)
    )
    response = requests.get(google_url, {"User-Agent": ua.random})
    soup = BeautifulSoup(response.text, "html.parser")
    result_div = soup.find_all("div", attrs={"class": "ZINbbc"})
    links = []
    titles = []
    descriptions = []
    for r in result_div:
        try:
            link = r.find("a", href=True)
            title = r.find("div", attrs={"class": "vvjwJb"}).get_text()
            description = r.find("div", attrs={"class": "s3v9rd"}).get_text()
            if link != "" and title != "" and description != "":
                links.append(link["href"])
                titles.append(title)
                descriptions.append(description)

        except:
            continue
    to_remove = []
    clean_links = []
    for i, l in enumerate(links):
        clean = re.search("\/url\?q\=(.*)\&sa", l)
        if clean is None:
            to_remove.append(i)
            continue
        clean_links.append(clean.group(1))
    for x in to_remove:
        del titles[x]
        del descriptions[x]
    msg = "".join(
        f"[{tt}]({liek})\n`{d}`\n\n"
        for tt, liek, d in zip(titles, clean_links, descriptions)
    )


    await pablo.edit("**Search Query:**\n`" + query + "`\n\n**Results:**\n" + msg)

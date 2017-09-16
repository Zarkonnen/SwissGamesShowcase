# -*- coding: utf-8 -*-

import re, csv, os, subprocess, requests

# Image processing horrors

def img_dims(src):
    name = "tmp/" + src.replace("/", "_").replace(":", "")
    if not os.path.exists(name):
        r2 = requests.get(src, timeout=8)
        if r2.status_code == 200:
            with open(name, 'wb') as f:
                f.write(r2.content)
    w, h = [int(x) for x in subprocess.check_output(["java", "-cp", ".", "ImgSize", name]).split(" ")]
    return (w, h)

def img(url):
    original = "tmp/" + url.replace("/", "_").replace(":", "")
    dst = "img/media/" + re.sub("[^a-zA-Z0-9.]", "", url)
    fmt = url.split("?")[0].split(".")[-1].lower()
    if not fmt in ["jpg", "png", "gif"]:
        fmt = "png"
        dst = dst + ".png"
    if not os.path.exists(original):
        print "Getting", url
        r = requests.get(url, timeout=8)
        if r.status_code == 200:
            with open(original, 'wb') as f:
                print "->", original
                f.write(r.content)
        else:
            print r.status_code
            return "img/unknown.png"
    if not os.path.exists(dst):
        try:
            subprocess.check_output(["java", "-cp", ".", "Resize", original, "480", "270", dst, fmt])
            print "->", dst
        except:
            print "Failed to resize", original
            return original
    return dst

M_HEADER = """<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8"> 
        <title>Swiss Games Showcase</title>
        <link href="https://fonts.googleapis.com/css?family=Raleway" rel="stylesheet">
        <link rel="stylesheet" href="style2.css">
    </head>
    <body>
        <div class="content">
        <h1>Swiss Games Showcase</h1>
        <div class="grid">"""

M_FOOTER = """
        </div>
        <div style="clear: both;">&nbsp;</div>
        <div class="info">An OpenGLAM Hackathon <a href="http://make.opendata.ch/wiki/project:swissvideogamesdirectory">project</a>.</div>
        </div>
    </body>
</html>"""

P_HEADER = """<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8"> 
        <title>{Title}</title>
        <link href="https://fonts.googleapis.com/css?family=Raleway" rel="stylesheet">
        <link rel="stylesheet" href="style2.css">
    </head>
    <body>
        <div class="big_content">
        <h1>{Title}</h1>
        <div class="big_card">"""

P_FOOTER = """
        <div class="back"><a href="index.html">More Swiss Games</a></div>
        </div>
        </div>
    </body>
</html>"""

def get_creators(developer):
    return re.split(" ?[,+/&:] ?", developer)

def store_name(url):
    if "itunes" in url:
        return "App Store"
    if "play.google" in url:
        return "Play Store"
    if "store.steampowered" in url:
        return "Steam"
    if "itch.io" in url:
        return "itch.io"
    if "playstation" in url:
        return "PlayStation"
    if "xbox.com" in url:
        return "Xbox"
    if "microsoft.com" in url:
        return "Xbox"
    return "Other Store"

def sort_date(g):
    if "Release Date" in g:
        d = g["Release Date"]
    elif "Early Access Date" in g:
        d = g["Early Access Date"]
    else:
        return ""
    d = d.strip()
    if not "-" in d and len(d) > 0:
        return d + "-01-01"
    return d

# Load and filter games
with open("Swiss Video Games - released-swiss-video-games.tsv") as f:
    games = list(csv.DictReader(f, delimiter='\t'))

for game in games:
    for k in list(game.keys()):
        if not game[k] or game[k].strip() == "":
            del game[k]

games.sort(key=sort_date)
games = games[::-1]

games = [g for g in games if ("Release Date" in g or "Early Access Date" in g) and "Website" in g and ("Trailer Video Link" in g or "Screenshot Direct Link" in g or "Box Art Direct Link" in g)]

# Index by creator
creator_to_games = {}
creator_to_id = {}
id_counter = 1
for game in games:
    cs = get_creators(game["Development Studio"])
    for c in cs:
        if not c in creator_to_id:
            creator_to_id[c] = id_counter
            id_counter += 1
        if not c in creator_to_games:
            creator_to_games[c] = [game["Identifier"]]
        else:
            creator_to_games[c].append(game["Identifier"])

# Generate site
with open("index.html", "w") as f:
    f.write(M_HEADER)

    for g in games:
        def w(s, **kwargs):
            info = g.copy()
            info.update(kwargs)
            f.write(s.format(**info))

        w('<div id="{Identifier}_card" class="card">')
        w('<a href="{Identifier}.html"><h2 class="card_title">{Title}</h2></a>')
        w('<div class="card_picture">')
        if "Box Art Direct Link" in g:
            w('<a href="{Identifier}.html"><img src="{src}" class="card_picture"></a>', src=img(g["Box Art Direct Link"]))
        elif "Screenshot Direct Link" in g:
            w('<a href="{Identifier}.html"><img src="{src}" class="card_picture"></a>', src=img(g["Screenshot Direct Link"]))
        elif "Trailer Video Link" in g:
            tvl = g["Trailer Video Link"]
            if "youtube" in tvl:
                w('<iframe class="card_yt" src="https://www.youtube.com/embed/{yt}?rel=0&amp;showinfo=0" frameborder="0" allowfullscreen></iframe>', yt=tvl.replace("https://www.youtube.com/watch?v=", "").split("?")[0])
            elif "vimeo" in tvl:
                w('<iframe class="card_vimeo" src="https://player.vimeo.com/video/{vimeo}" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen class="card_vimeo"></iframe>', vimeo=tvl.replace("https://player.vimeo.com/video/", "").replace("https://vimeo.com/", "").replace("/", ""))
        elif "Logo Direct Link" in g:
            w('<a href="{Identifier}.html"><img src="{src}" class="card_picture"></a>', src=img(g["Logo Direct Link"]))
        w('</div>')
        w('<div class="card_details">')
        w('<p>{Development Studio}</p>')
        if "Release Date" in g:
            w('<p>{Release Date}</p>')
        else:
            w('<p>{Early Access Date}</p>')
        w('<p>{Platforms}</p>')
        if "Online Play" in g:
            w('<p><a href="{Online Play}">Play Online</a></p>')
        if "Download Page" in g:
            w('<p><a href="{Download Page}">Download</a></p>')
        if "Direct Download" in g:
            w('<p><a href="{Direct Download}">Download</a></p>')
        if "Store" in g:
            w('<p>')
            stores = [s.strip() for s in g["Store"].split(",")]
            for s in stores:
                w('<a href="{link}">{name}</a>', name=store_name(s), link=s)
                if not s == stores[-1]:
                    w(', ')
            w('</p>')
        w('</div>')
        w('<div style="clear: both;"></div>')
        w('</div>')
        with open(g["Identifier"] + ".html", "w") as f2:
            def w(s, **kwargs):
                info = g.copy()
                info.update(kwargs)
                f2.write(s.format(**info))
            w(P_HEADER)
            w('<div class="big_card_left">')
            w('<div class="big_card_picture">')
            if "Trailer Video Link" in g:
                tvl = g["Trailer Video Link"]
                if "youtube" in tvl:
                    w('<iframe class="big_card_yt" src="https://www.youtube.com/embed/{yt}?rel=0&amp;showinfo=0" frameborder="0" allowfullscreen></iframe>', yt=tvl.replace("https://www.youtube.com/watch?v=", "").split("?")[0])
                elif "vimeo" in tvl:
                    w('<iframe class="card_vimeo" src="https://player.vimeo.com/video/{vimeo}" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen class="big_card_vimeo"></iframe>', vimeo=tvl.replace("https://player.vimeo.com/video/", "").replace("https://vimeo.com/", "").replace("/", ""))
            elif "Box Art Direct Link" in g:
                w('<a href="{Identifier}.html"><img src="{src}" class="big_card_picture"></a>', src=img(g["Box Art Direct Link"]))
            elif "Screenshot Direct Link" in g:
                w('<a href="{Identifier}.html"><img src="{src}" class="big_card_picture"></a>', src=img(g["Screenshot Direct Link"]))
            elif "Logo Direct Link" in g:
                w('<a href="{Identifier}.html"><img src="{src}" class="big_card_picture"></a>', src=img(g["Logo Direct Link"]))
            w('</div>')
            w('<p>{desc}</p>', desc=g["Description"].replace("\n", "<br") if "Description" in g else "")
            w('</div>')
            w('<div class="big_card_details">')
            w('<p>Developer: {Development Studio}</p>')
            if "Publisher" in g:
                w('<p>Publisher: {Publisher}</p>')
            if "Sponsor" in g:
                w('<p>Sponsor: {Sponsor}</p>')
            if "Release Date" in g:
                w('<p>Release Date: {Release Date}</p>')
            if "Early Access Date" in g:
                w('<p>Early Access Date: {Early Access Date}</p>')
            w('<p>Platforms: {Platforms}</p>')
            if "Awards" in g:
                w('<p>Awards: {Awards}</p>')
            if "Website" in g:
                w('<p><a href="{Website}">Website</a></p>')
            if "Online Play" in g:
                w('<p><a href="{Online Play}">Play Online</a></p>')
            if "Download Page" in g:
                w('<p><a href="{Download Page}">Download</a></p>')
            if "Direct Download" in g:
                w('<p><a href="{Direct Download}">Download</a></p>')
            if "Store" in g:
                w('<p>')
                stores = [s.strip() for s in g["Store"].split(",")]
                for s in stores:
                    w('<a href="{link}">{name}</a>', name=store_name(s), link=s)
                    if not s == stores[-1]:
                        w(', ')
                w('</p>')
            if "Source" in g:
                w('<p><a href="{Source}">Source</a></p>')
            if "Development Log" in g:
                w('<p><a href="{Development Log}">Development Log</a></p>')
            if "Press Kit" in g:
                w('<p><a href="{Presskit}">Press Kit</a></p>')
            if "Twitter" in g:
                w('<p><a href="{Twitter}">Twitter</a></p>')
            if "Article Links" in g:
                w('<p>Articles:')
                w('<ul>')
                for a in g["Article Links"].split(","):
                    a = a.strip()
                    w('<li><a href="{link}">{name}</a></li>', link=a, name=a.replace("https://", "").replace("http://", "").replace("www.", "").split(".")[0])
                w('</ul></p>')
            w('</div>')
            w('<div style="clear: both;"></div>')
            w(P_FOOTER)

    f.write(M_FOOTER)

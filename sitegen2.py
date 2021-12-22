# -*- coding: utf-8 -*-

import re, csv, os, subprocess, requests

# Image processing horrors

def img_dims(src):
    name = "download/" + src.replace("/", "_").replace(":", "")
    if not os.path.exists(name):
        r2 = requests.get(src, timeout=8)
        if r2.status_code == 200:
            with open(name, 'wb') as f:
                f.write(r2.content)
    w, h = [int(x) for x in subprocess.check_output(["java", "-cp", ".", "ImgSize", name]).split(" ")]
    return (w, h)

def img(url):
    original = "download/" + url.replace("/", "_").replace(":", "")
    dst = "img/media/" + re.sub("[^a-zA-Z0-9.]", "", url)
    fmt = url.split("?")[0].split(".")[-1].lower()
    if not fmt in ["jpg", "png", "gif"]:
        fmt = "png"
        dst = dst + ".png"
    if not os.path.exists(original):
        print("Getting", url, original)
        r = requests.get(url, timeout=8)
        if r.status_code == 200:
            with open(original, 'wb') as f:
                print("->", original)
                f.write(r.content)
        else:
            print(r.status_code)
            return "img/unknown.png"
    if not os.path.exists(dst):
        try:
            subprocess.check_output(["java", "-cp", ".", "Resize", original, "400", "225", dst, fmt])
            subprocess.check_output(["java", "-cp", ".", "Resize", original, "800", "450", "big-" + dst, fmt])
            print("->", dst)
        except:
            print("Failed to resize", original)
            return original
    return dst

def has_img(url):
    return img(url) != "img/unknown.png"

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
    if "itunes" in url or "apps.apple" in url or "apple.co" in url:
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
    if "oculus" in url:
        return "Oculus"
    if "nintendo.com" in url:
        return "Nintendo"
    if "apps.facebook" in url:
        return "Facebook"
    if "amazon" in url:
        return "Amazon"
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
    elif len(d.split("-")) == 2:
        return d + "-01"
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

with open("report.txt", "w") as report:
    for g in games:
        if not "Title" in g:
            continue
        title = g["Title"]
        if "Genres" in g and "porn" in g["Genres"].lower():
            report.write(title + ": Not listing porn game: " + g["Genres"] + "\n")
        if not ("Release Date" in g or "Early Access Date" in g):
            report.write(title + ": No release or early access date.\n")
        if not "Website" in g:
            report.write(title + ": No website.\n")
        if not "Store" in g and not "Source" in g and not "Online Play" in g and not "Download Page" in g and not "Direct Download" in g:
            report.write(title + ": No store, source, online play or download links.\n")
        if not "Description" in g:
            report.write(title + ": No description.\n")
        if not ("Trailer Video Link" in g or "Screenshot Direct Link" in g or "Box Art Direct Link" in g):
            report.write(title + ": No trailer, screenshot, or box art.\n")
        else:
            if not ("Screenshot Direct Link" in g or "Box Art Direct Link" in g):
                report.write(title + ": No screenshot or box art.\n")
    games = [g for g in games if "Title" in g and ("Release Date" in g or "Early Access Date" in g) and ("Trailer Video Link" in g or "Screenshot Direct Link" in g or "Box Art Direct Link" in g)]

    # Index by creator
    creator_to_games = {}
    creator_to_id = {}
    id_counter = 1
    for game in games:
        if "Development Studio" in game:
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
            
            if not ("Genres" in g and "porn" in g["Genres"].lower()):
                w('<div id="{Identifier}_card" class="card">')
                w('<div class="card_picture">')
                if "Box Art Direct Link" in g and has_img(g["Box Art Direct Link"]):
                    w('<a href="{Identifier}.html"><img src="{src}" class="card_picture"></a>', src=img(g["Box Art Direct Link"]))
                elif "Screenshot Direct Link" in g and has_img(g["Screenshot Direct Link"]):
                    w('<a href="{Identifier}.html"><img src="{src}" class="card_picture"></a>', src=img(g["Screenshot Direct Link"]))
                elif "Trailer Video Link" in g:
                    tvl = g["Trailer Video Link"]
                    if "youtube" in tvl:
                        w('<iframe class="card_yt" src="https://www.youtube.com/embed/{yt}?rel=0&amp;showinfo=0" frameborder="0" allowfullscreen></iframe>', yt=tvl.replace("https://www.youtube.com/watch?v=", "").split("?")[0])
                    elif "vimeo" in tvl:
                        w('<iframe class="card_vimeo" src="https://player.vimeo.com/video/{vimeo}" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen class="card_vimeo"></iframe>', vimeo=tvl.replace("https://player.vimeo.com/video/", "").replace("https://vimeo.com/", "").replace("/", ""))
                    else:
                        report.write(g["Title"] + ": Unknown trailer URL format.\n")
                elif "Logo Direct Link" in g and has_img(g["Logo Direct Link"]):
                    w('<a href="{Identifier}.html"><img src="{src}" class="card_picture"></a>', src=img(g["Logo Direct Link"]))
                else:
                    w('<a href="{Identifier}.html"><img src="img/unknown.png" class="card_picture"></a>')
                    report.write(g["Title"] + ": Unable to fetch images.\n")
                w('</div>')
                w('<div class="card_details">')
                w('<a href="{Identifier}.html"><h2 class="card_title">{Title}</h2></a>')
                if "Development Studio" in g:
                    w('<p>{Development Studio}</p>')
                if "Release Date" in g:
                    w('<p>{Release Date}</p>')
                else:
                    w('<p>{Early Access Date}</p>')
                if "Platforms" in g:
                    w('<p>{Platforms}</p>')
                w('<p>')
                comma = False
                if "Online Play" in g:
                    if comma:
                        w(', ')
                    w('<a href="{Online Play}">Play Online</a>')
                    comma = True
                if "Download Page" in g:
                    if comma:
                        w(', ')
                    w('<a href="{Download Page}">Download</a>')
                    comma = True
                if "Direct Download" in g:
                    if comma:
                        w(', ')
                    w('<a href="{Direct Download}">Download</a>')
                    comma = True
                if "Store" in g:
                    stores = [s.strip() for s in g["Store"].split(",")]
                    for s in stores:
                        if comma:
                            w(', ')
                        w('<a href="{link}">{name}</a>', name=store_name(s), link=s)
                        comma = True
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
                elif "Box Art Direct Link" in g and has_img(g["Box Art Direct Link"]):
                    w('<a href="{Identifier}.html"><img src="big-{src}" class="big_card_picture"></a>', src=img(g["Box Art Direct Link"]))
                elif "Screenshot Direct Link" in g and has_img(g["Screenshot Direct Link"]):
                    w('<a href="{Identifier}.html"><img src="big-{src}" class="big_card_picture"></a>', src=img(g["Screenshot Direct Link"]))
                elif "Logo Direct Link" in g and has_img(g["Logo Direct Link"]):
                    w('<a href="{Identifier}.html"><img src="big-{src}" class="big_card_picture"></a>', src=img(g["Logo Direct Link"]))
                w('</div>')
                w('<p>{desc}</p>', desc=g["Description"].replace("\n", "<br") if "Description" in g else "")
                w('</div>')
                w('<div class="big_card_details">')
                if "Development Studio" in g:
                    w('<p>Developer: {Development Studio}</p>')
                if "Publisher" in g:
                    w('<p>Publisher: {Publisher}</p>')
                if "Sponsor" in g:
                    w('<p>Sponsor: {Sponsor}</p>')
                if "Release Date" in g:
                    w('<p>Release Date: {Release Date}</p>')
                if "Early Access Date" in g:
                    w('<p>Early Access Date: {Early Access Date}</p>')
                if "Platforms" in g:
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
                    if "@" in g["Twitter"]:
                        w('<p><a href="https://twitter.com/{name}">Twitter</a></p>', name=g["Twitter"].replace("@", ""))
                    else:
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

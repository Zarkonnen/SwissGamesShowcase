print """<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8"> 
        <title>Swiss Games Showcase</title>
        <link rel="stylesheet" href="style.css">
    </head>
    <body>
        <h1>Swiss Games Showcase</h1>
        <div class="grid">
"""

import csv, cgi

with open("out.csv") as f:
    games = sorted(list(csv.DictReader(f)), key=lambda x: x["Year"])[::-1]
    for game in games:
        if not game["Year"]:
            continue
        print """<div class="game">"""
        print """<a href="{URL}" class="gamename">{Name}</a><div class="developername">{Developer} {Year}</div>""".format(**game)
        if game["Vimeo"]:
            print """<iframe class="ytframe" src="{0}" width="320" height="180" frameborder="0" webkitAllowFullScreen mozallowfullscreen allowFullScreen></iframe>""".format(game["Vimeo"].replace("autoplay=1", "autoplay=0"))
        elif game["YouTube"]:
            print """<iframe width="320" height="180" class="ytframe" src="https://www.youtube.com/embed/{0}?rel=0&amp;showinfo=0" frameborder="0" allowfullscreen></iframe>""".format(game["YouTube"].replace("https://www.youtube.com/watch?v=", "").split("?")[0])
        elif game["Screenshot"]:
            print """<div class="screenshotcontainer"><a href="{URL}"><img src="{Screenshot}"></a></div>""".format(**game)
        else:
            print """<div class="noscreenshot">&nbsp;</div>"""
        if game["Apple"]:
            print """<a href="{Apple}" class="apple">App Store</a>""".format(**game)
        if game["Google"]:
            print """<a href="{Google}" class="google">Google Play</a>""".format(**game)
        if game["Steam"]:
            print """<a href="{Steam}" class="apple">Steam</a>""".format(**game)
        print """</div>"""


print """
        </div>
        <div style="clear: both;">&nbsp;</div>
        <div class="info">An OpenGLAM Hackathon project by <a href="http://www.zarkonnen.com">David Stark</a>.</div>
    </body>
</html>
"""

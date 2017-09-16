# -*- coding: utf-8 -*-

print """<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8"> 
        <meta name="viewport" content = "width = device-width, initial-scale = 1.0, user-scalable = no" />
        <title>Swiss Games Showcase</title>
        <link rel="stylesheet" href="style.css">
        <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
    </head>
    <body>
        <h1>Swiss Games Showcase</h1>
        <div id="filter"><span id="filtername"></span> <span id="clear_filter" onclick="clear_filter()">[x]</span></div>
        <div class="grid">
"""

import json, re, csv

def get_creators(developer):
    return re.split(" ?[,+/&:] ?", developer)

def buyname(url):
    if "itunes" in url:
        return "App Store"
    if "play.google" in url:
        return "Play Store"
    if "store.steampowered" in url:
        return "Steam"
    if "itch.io" in url:
        return "itch.io"
    return "Other Store"

with open("Swiss Video Games - released-swiss-video-games.tsv") as f:
    games = sorted(csv.DictReader(f, delimiter='\t'), key=lambda x: x["Release Date"] if "Release Date" in x else "")[::-1]
    creator_to_games = {}
    creator_to_id = {}
    id_counter = 1
    for game in games:
        for k in list(game.keys()):
            if not game[k]:
                del game[k]
        if not "Release Date" in game:
            continue
        cs = get_creators(game["Development Studio"])
        for c in cs:
            if not c in creator_to_id:
                creator_to_id[c] = id_counter
                id_counter += 1
            if not c in creator_to_games:
                creator_to_games[c] = [game["Identifier"]]
            else:
                creator_to_games[c].append(game["Identifier"])
    col_index = 0
    row_index = 0
    print """<div id="row{0}">""".format(row_index)
    for game in games:
        if not "Release Date" in game:
            continue
        if not "Website" in game:
            continue
        if not "Trailer Video Link" in game and not "Screenshot Direct Link" in game:
            continue
        cs = get_creators(game["Development Studio"])
        print """<div class="game {0}">""".format(" ".join("c" + str(creator_to_id[c]) for c in cs)) 
        print """<div class="gamename"><a href="{Website}">{Title}</a></div><div class="developername">""".format(**game)
        for c in cs:
            if len(creator_to_games[c]) > 1:
                print """<span class="creator" onclick="filter_creator({0}, '{1}')">{1}</span>""".format(creator_to_id[c], c.replace("'", "’"))
            else:
                print c
            if c != cs[-1]:
                print "/ "
        print """ {Release Date}</div>""".format(**game)
        if "Trailer Video Link" in game:
            if "youtube" in game["Trailer Video Link"]:
                print """<iframe class="ytframe" src="https://www.youtube.com/embed/{0}?rel=0&amp;showinfo=0" frameborder="0" allowfullscreen></iframe>""".format(game["Trailer Video Link"].replace("https://www.youtube.com/watch?v=", "").split("?")[0])
            elif "vimeo" in game["Trailer Video Link"]:
                print """<iframe class="ytframe" src="{0}" frameborder="0" webkitAllowFullScreen mozallowfullscreen allowFullScreen></iframe>""".format(game["Trailer Video Link"].replace("autoplay=1", "autoplay=0"))
        elif "Screenshot Direct Link" in game:
            print """<div class="screenshotcontainer"><a href="{Website}"><img src="{Screenshot Direct Link}"></a></div>""".format(**game)
        else:
            print """<div class="noscreenshot">&nbsp;</div>"""
        print """<div class="buy">"""
        if "Store" in game:
            for st in game["Store"].split(","):
                print """<a href="{0}" class="store">{1}</a>""".format(st, buyname(st))
        print """</div></div>"""
        col_index += 1
        if col_index == 3:
            row_index += 1
            col_index = 0
            print """</div><div id="row{0}" class="row" style="display: none;">""".format(row_index)

print """<script>var rows = {0};</script>""".format(row_index)
print """
</div>
        </div>
        <div style="clear: both;">&nbsp;</div>
        <div id="loading" style="text-align: center;">Loading...</div>
        <div class="info">An OpenGLAM Hackathon <a href="http://make.opendata.ch/wiki/project:swissgamesshowcase">project</a> by <a href="http://www.zarkonnen.com">David Stark</a>.</div>
        <script>
            var loading_all_done = false;
            var row_index = 0;
            function load_more(callback) {
                jQuery("#row" + row_index).show();
                row_index++;
                if (row_index >= rows) {
                    loading_all_done = true;
                    jQuery("#loading").hide();
                }
                if (callback) { callback(); }
            }
            function load_if_screen_not_full() {
                if (!loading_all_done && $("body").height() < $(window).height() + 400) {
                    load_more(load_if_screen_not_full);
                }
            }
            $(document).ready(function() {
                load_if_screen_not_full();
	            $(window).scroll(function () {
		            if (!loading_all_done && $(window).scrollTop() >= $(document).height() - $(window).height() - 10) {
			            load_more();
		            }
	            });
            });
            function filter_creator(id, name) {
                jQuery('.game').hide();
                jQuery('.row').show();
                jQuery('.c' + id).show();
                jQuery('#filtername').html(name);
                jQuery('#filter').show();
                jQuery("#loading").hide();
            }
            function clear_filter() {
                jQuery('.game').show();
                jQuery('.row').show();
                jQuery('#filter').hide();
            }
        </script>
    </body>
</html>
"""

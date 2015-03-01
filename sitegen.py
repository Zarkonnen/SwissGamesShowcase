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

import json, re

with open("patch.json") as f:
    patches = {e["name"]:e for e in json.load(f)}

def get_creators(developer):
    return re.split(" ?[,+/&:] ?", developer)

with open("out.json") as f:
    games = sorted(json.load(f), key=lambda x: x["year"] if "year" in x else "")[::-1]
    creator_to_games = {}
    creator_to_id = {}
    id_counter = 1
    for game in games:
        if game["name"] in patches:
            for k, v in patches[game["name"]].iteritems():
                game[k] = v
        if not "year" in game:
            continue
        for k in game:
            game[k] = game[k].encode('utf-8')
        cs = get_creators(game["developer"])
        for c in cs:
            if not c in creator_to_id:
                creator_to_id[c] = id_counter
                id_counter += 1
            if not c in creator_to_games:
                creator_to_games[c] = [game["name"]]
            else:
                creator_to_games[c].append(game["name"])
    col_index = 0
    row_index = 0
    print """<div id="row{0}">""".format(row_index)
    for game in games:
        if not "year" in game:
            continue
        cs = get_creators(game["developer"])
        print """<div class="game {0}">""".format(" ".join("c" + str(creator_to_id[c]) for c in cs)) 
        print """<div class="gamename"><a href="{url}">{name}</a></div><div class="developername">""".format(**game)
        for c in cs:
            if len(creator_to_games[c]) > 1:
                print """<span class="creator" onclick="filter_creator({0}, '{1}')">{1}</span>""".format(creator_to_id[c], c.replace("'", "’"))
            else:
                print c
            if c != cs[-1]:
                print "/ "
        print """ {year}</div>""".format(**game)
        if "vimeo" in game:
            print """<iframe class="ytframe" src="{0}" frameborder="0" webkitAllowFullScreen mozallowfullscreen allowFullScreen></iframe>""".format(game["vimeo"].replace("autoplay=1", "autoplay=0"))
        elif "youtube" in game:
            print """<iframe class="ytframe" src="https://www.youtube.com/embed/{0}?rel=0&amp;showinfo=0" frameborder="0" allowfullscreen></iframe>""".format(game["youtube"].replace("https://www.youtube.com/watch?v=", "").split("?")[0])
        elif "screenshot" in game:
            print """<div class="screenshotcontainer"><a href="{url}"><img src="{screenshot}"></a></div>""".format(**game)
        else:
            print """<div class="noscreenshot">&nbsp;</div>"""
        print """<div class="buy">"""
        if "apple" in game:
            print """<a href="{apple}" class="apple">App Store</a>""".format(**game)
        if "google" in game:
            print """<a href="{google}" class="google">Google Play</a>""".format(**game)
        if "steam" in game:
            print """<a href="{steam}" class="apple">Steam</a>""".format(**game)
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

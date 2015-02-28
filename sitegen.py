print """<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8"> 
        <title>Swiss Games Showcase</title>
        <link rel="stylesheet" href="style.css">
        <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
    </head>
    <body>
        <h1>Swiss Games Showcase</h1>
        <div class="grid">
"""

import json

with open("patch.json") as f:
    patches = {e["name"]:e for e in json.load(f)}

with open("out.json") as f:
    games = sorted(json.load(f), key=lambda x: x["year"] if "year" in x else "")[::-1]
    col_index = 0
    row_index = 0
    print """<div id="row{0}">""".format(row_index)
    for game in games:
        if game["name"] in patches:
            for k, v in patches[game["name"]].iteritems():
                game[k] = v
        if not "year" in game:
            continue
        for k in game:
            game[k] = game[k].encode('utf-8')
        print """<div class="game">"""
        print """<a href="{url}" class="gamename">{name}</a><div class="developername">{developer} {year}</div>""".format(**game)
        if "vimeo" in game:
            print """<iframe class="ytframe" src="{0}" width="320" height="180" frameborder="0" webkitAllowFullScreen mozallowfullscreen allowFullScreen></iframe>""".format(game["vimeo"].replace("autoplay=1", "autoplay=0"))
        elif "youtube" in game:
            print """<iframe width="320" height="180" class="ytframe" src="https://www.youtube.com/embed/{0}?rel=0&amp;showinfo=0" frameborder="0" allowfullscreen></iframe>""".format(game["youtube"].replace("https://www.youtube.com/watch?v=", "").split("?")[0])
        elif "screenshot" in game:
            print """<div class="screenshotcontainer"><a href="{url}"><img src="{screenshot}"></a></div>""".format(**game)
        else:
            print """<div class="noscreenshot">&nbsp;</div>"""
        if "apple" in game:
            print """<a href="{apple}" class="apple">App Store</a>""".format(**game)
        if "google" in game:
            print """<a href="{google}" class="google">Google Play</a>""".format(**game)
        if "steam" in game:
            print """<a href="{steam}" class="apple">Steam</a>""".format(**game)
        print """</div>"""
        col_index += 1
        if col_index == 3:
            row_index += 1
            col_index = 0
            print """</div><div id="row{0}" style="display: none;">""".format(row_index)

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
        </script>
    </body>
</html>
"""

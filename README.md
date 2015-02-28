Swiss Games Showcase
--------------------
A website made to show off the work of the growing Swiss computer game scene. The basis of the site is a crowdsourced list of Swiss games. This list is parsed, and additional information on each game is automatically gathered. Finally, a static showcase page is generated.

### Setup
The project requires Python, Java, and the beautifulsoup4 and requests Python libraries. Both libraries can be installed via pip. Also, create a "tmp" directory to act as a cache for downloaded images.

### Usage
* Re-export the list of Swiss games to HTML and save it as `ReleasedSwissVideoGames.html`.
* Invoke `python crawl.py`. This will parse the HTML file and crawl the games' sites for media. This process takes a while and results in `out.csv`and `out.json`, two structured lists of information about the games.
* Invoke `python sitegen.py` to re-generate `index.html`.

### About
This project was created by [David Stark](http://www.zarkonnen.com) for the [1st Swiss Open Cultural Data Hackathon](http://make.opendata.ch/wiki/event:2015-02) 2015.

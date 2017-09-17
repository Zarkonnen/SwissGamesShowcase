Swiss Games Showcase
--------------------
A website made to show off the work of the growing Swiss computer game scene. The basis of the site is a [crowdsourced table](https://docs.google.com/spreadsheets/d/1pWOGpADxvNEWcYnpTFpCyhS9rtIjCYgIdZmBppDkC2Q/edit?usp=sharing) of Swiss games.

### Additions and Improvements
Want to add a game to this site? Add it to the table! We're especially looking for older games, pre-2010. Any game that was publicly available in some fashion and was created in Switzerland should be included.

### Setup
Running the project requires Python, Java, and the requests library. Also, create a "tmp" directory to act as a cache for downloaded images.

### Usage
* Re-export the table of Swiss games to TSV and save it as `Swiss Video Games - released-swiss-video-games.tsv`.
* Invoke `python sitegen2.py` to re-generate the site.

### About
This project was created by [David Stark](http://www.zarkonnen.com) for the [1st Swiss Open Cultural Data Hackathon](http://make.opendata.ch/wiki/event:2015-02) 2015.

It was then extended by David Stark, Karine Delvert, Selim Krichane, Oleg Lavrovsky, Frédéric Noyer, Isaac Pante, Yannick Rochat and Oliver Waddell for the [3rd OpenGLAM Hackathon](http://make.opendata.ch/wiki/project:swissvideogamesdirectory) in 2017.

ShowHound
============
###Summary
ShowHound is a search engine that helps you quickly find the next airing of an episode of your favorite, **popular** television program. 

![ShowHound Interface](/images/shound1.png)

ShowHound searches more than 500k movies and television shows (via keyword) to surface details about plots, actors, and episode rating information.

###Version
0.5


###Details
- [Technology](#technology)
- [Features](#features)
- [Screenshots](#screenshots)
- [Installation](#install)


###Technology

ShowHound uses a number of open source projects to work properly:

*	Python 2.7 <br>
*	Flask 0.9 <br>
*	AngularJS <br>
*	Twitter Bootstrap <br>
*	JavaScript <br>
* HTML/CSS <br>
*	jQuery <br>
*	MySQL <br>
*	RegEx <br>
* Flask-Login 0.2.11 <br>
* Flash-WTF 0.8 <br>
* Google Maps JS embed API  <br>
* Mapbox API (LeafletJS) <br>
*	OAuth 1.0.1 <br>
* OAuthlib 0.7.2 <br>
* StormPath API <br>
* TVMaze API <br>
* Twilio API


### Features
Single Page Application <br>
MySQL/PostgreSQL data storage <br> 
Full-Text search <br>
Autocomplete functionality (Series/Episodes) <br>
Secure user login functionality <br>
Facebook/Twitter Authentication <br>
Geolocation/Geocoding capabilities (Google Maps/LeafletJS) <br>
Save and view user favorites <br>
Customized notifications - future episode airings


### Screenshots
![ShowHound Interface](/images/shound6.png)
![ShowHound Interface](/images/shound5.png)
![ShowHound Interface](/images/shound3.png)



### Installation

Installing/Running ShowHound and it's dependencies:

```sh
$ git clone [git-repo-url] showhound 
```

```sh
$ pip install requirements.txt
```

```sh
$ git clone [git-repo-url] showhound
$ cd showhound
$ source env/bin/activate [env-dir]
$ python -i routes.py
```

### Plugins

ShowHound is currently extended with the following plugins

* PyQuery 1.2.9 <br>
* Scrapy 0.24.4 <br>
* Whoosh 2.6.0


### Todo's

- Extend keyword search capabilities
- Refactor to optimize API calls
- Complete AWS Elastic Beanstalk deployment





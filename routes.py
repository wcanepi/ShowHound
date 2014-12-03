# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, flash, abort, redirect, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from forms import ContactForm
from flask import session as flask_session
from flask.ext.stormpath import StormpathManager, StormpathError, User, login_required, login_user, logout_user, user
from flask.ext.mail import Message, Mail
# from geodata import get_geodata
import urllib2
import omdb
import requests
import urllib
import re
import json
import sys
from os import environ 
import codecs
from model import Series, Shows, Users, session as dbsession
from pyquery import PyQuery as pq




mail = Mail()
# from shound.models import base
 
app = Flask(__name__)
app.config['SQLAlCHEMY_DATABASE_URI'] = 'mysql://user:pass@localhost:3306/showhound'
 


# app.secret_key = 'thisASQWERYTYsecret'

app.config['SECRET_KEY'] = 'thisASQWERYTYsecret'
app.config['STORMPATH_API_KEY_FILE'] = '~/.stormpath/apiKey.properties'
app.config['STORMPATH_APPLICATION'] = 'ShowHound'

stormpath_manager = StormpathManager(app)

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'contact@example.com'
app.config["MAIL_PASSWORD"] = 'your-password'
 
mail.init_app(app)

""" {'Plot': 'Six young people, on their own and struggling to survive in the
real world, find the companionship, comfort and support they get from each other
to be the perfect antidote to the pressures of life.', 'Rated': 'TV-14',
u'Response': 'True', 'Language': 'English', 'Title': 'Friends', 'Country':
u'USA', 'Writer': 'David Crane, Marta Kauffman', 'Metascore': 'N/A',
u'imdbRating': '9.0', 'Director': 'N/A', 'Released': '22 Sep 1994',
u'Actors': 'Jennifer Aniston, Courteney Cox, Lisa Kudrow, Matt LeBlanc',
u'Year': '1994\u20132004', 'Genre': 'Comedy, Romance', 'Awards': 'Won 1
Golden Globe. Another 62 wins & 174 nominations.', 'Runtime': '22 min',
u'Type': 'series', 'Poster': 'http://ia.media-imdb.com/images/M/MV5BMzgxMzcxM
jYzMl5BMl5BanBnXkFtZTcwMzE3NTEyMQ@@._V1_SX300.jpg', 'imdbVotes': '329,539',
u'imdbID': 'tt0108778'} """

@app.route("/london")
def index():
  searchshow = request.args.get("searchshow")
  if not searchshow:
      searchshow = "Seinfeld"
  data = json.loads(get_omdb(searchshow))
  print data
  try:
    show = data['title']['name']
  except KeyError:
    return render_template("invalid_show.html")
  show_list = []
  for d in data.get("list"): 
    title = d.get("Title")
    year = d.get("Year")
    actors = d.get("Actors")
    imdb_rating = d.get("imdbRating")
    plot = d.get("Plot")
    imdbID = d.get("imdbID")
    showtype = d.data.get("Type")
    genre = d.get("Genre")
    print show_list
  return render_template("london.html", show_list=show_list, title=title, year=year, imdb_rating=imdb_rating, actors=actors, plot=plot, imdbID=imdbID, showtype=showtype, genre=genre)


@app.route('/')
def home():  
  show_list = dbsession.query(Shows).all()
  return render_template('home.html')

@app.route('/show_list')
def show_list():
  show_list = dbsession.query(Shows).all()
  # return render_template('home.html')
  return render_template("show_list.html", shows=show_list)

@app.route('/api/search/title')
def api_title_results():
  if "searchshow" not in request.args:
    return "No title sent"

  title = request.args.get("searchshow")
  omdbData = get_omdb(title)

  data = json.loads(omdbData)
  # listings = getListings("http://www.imdb.com/title/"+data["imdbID"]+"/tvschedule")
  # data['Listings'] = listings
  return json.dumps(data)

def row2dict(row):
  d = {}
  for column in row.__table__.columns:
      d[column.name] = str(getattr(row, column.name))

  return d

@app.route("/api/search/listings")
def api_listing_results():
  if "imdb_id" not in request.args:
    return "No imdb ID sent"
  
  listings = getListings("http://www.imdb.com/title/"+request.args.get("imdb_id")+"/tvschedule")
  return json.dumps(listings)

@app.route('/api/search/showkeyword')
def api_keyword_results():
  if "imdb_id" not in request.args:
    return "No imdb ID sent"

  if "keywords" not in request.args:
    return "No keywords sent"

  imdb_id = request.args.get("imdb_id")
  keywords = request.args.get("keywords")

  results = dbsession.query(Series).filter(Series.seriesid==Shows.id).filter(Shows.imdb_id==imdb_id)
  keywords = keywords.split()
  for i in range(len(keywords)):
    results = results.filter(Series.plot.like('%'+keywords[i]+'%'))

  results = results.all()

  rtnResults = []
  for i in results:
    rtnResults.append(row2dict(i))

  return json.dumps(rtnResults)


@app.route('/about')
def about():
  return render_template('about.html')

def get_omdb(searchshow):
  url = "http://www.omdbapi.com/?t="+urllib2.quote(searchshow)+"&plot=full&r=json"
  response = urllib2.urlopen(url).read()
  return response

def getListings(url):
  response = urllib2.urlopen(url).read()
  d = pq(response)
  rows = d(".dataTable tr")
  listings = []
  for row in rows:
    tds = row.findall("td")
    listing = []
    
    epinfo = d(tds[3]).text()

    m = re.match(r"(.+)\(S([0-9])(.*)Ep([0-9]+)\)", "epinfo")

    listings.append([d(tds[0]).text(),d(tds[1]).text(),d(tds[2]).text(),epinfo,m.group(2),m.group(4)])

  return listings

@app.route('/new')
def new():
  return render_template('about.html')
  data = json.loads(get_friends())
  page = "<html><head><title>Friends</title></head><body>"
  page += "<h1> Details for {}, {}</h1>".format(data.get('title').get('Actors'), data.get('title').get('Actors'))
  for  show in data.get("list"):
    page += "<b> Genre:</b>"
  page += "</body></html>"
  return page


@app.route('/contact', methods=['GET', 'POST'])
def contact():
  form = ContactForm()
 
  if request.method == 'POST':
    if form.validate() == False:
      flash('All fields are required.')
      return render_template('contact.html', form=form)
    else:
      msg = Message(form.subject.data, sender='contact@example.com', recipients=['your_email@example.com'])
      msg.body = """
      From: %s &lt;%s&gt;
      %s
      """ % (form.name.data, form.email.data, form.message.data)
      mail.send(msg)
 
      return render_template('contact.html', success=True)
 
  elif request.method == 'GET':
    return render_template('contact.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        try:
            _user = User.from_login(
                request.form['email'],
                request.form['password'],
            )
            login_user(_user, remember=True)
            flash('You were logged in.')

            return redirect(url_for('show_posts'))
        except StormpathError, err:
            error = err.message

    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    logout_user()
    flash('You were logged out.')

    return redirect(url_for('show_posts'))

@app.route('/list_series', methods=['GET','POST'])
def list_series():
    for i in range (1,5):
      try:
        url = 'http://api.tvmaze.com/shows/530/episodes' 
        response_dict = requests.get(url).json()
        json_obj = urllib2.urlopen(url)
        count = 0
        tv_episodes = json.load(json_obj)
        # print tv_episodes
        print " "
        if json_obj.code != '404':
          for episode in tv_episodes:
            episodes = episode['id'],episode['name'],episode['season'],episode['number'],episode['airdate'],episode['airtime'],episode['runtime']
            # print episodes
        return render_template("list_series.html", response_dict=response_dict)

      except urllib2.HTTPError, e:
        print 'We failed with error code - %s.' % e.code


@app.route('/get_show', methods=['GET','POST'])
def get_show():
    for i in range (1,600):
      try:
          url = 'http://api.tvmaze.com/shows/431'
          show_dict = requests.get(url).json()
          json_obj = urllib2.urlopen(url)
          count = 0
          print " "
          happy = convertkeys(show_dict)
          # print happy
          return render_template("get_show.html", happy=happy)
      except urllib2.HTTPError, e:
        print 'We failed with error code - %s.' % e.code


# @app.route('/get_series', methods=['GET','POST'])
# def get_series():
#   # for i in range (1,episode_page_cnt):
#     for i in range (1,5):
#       try:
#         url = 'http://api.tvmaze.com/shows/66/episodes' 
#         # url = 'http://api.tvmaze.com/shows/%d/episodes' % i
#         json_obj = urllib2.urlopen(url)
#         count = 0
#         tv_episodes = json.load(json_obj)
#         # print tv_episodes
#         print " "
#         if json_obj.code != '404':
#           for episode in tv_episodes:
#             # print episode['id'],episode['name'].encode("ascii", "ignore"),episode['season'],episode['number'],episode['airdate'].encode("ascii", "ignore"),episode['airtime'].encode("ascii","ignore"),episode['runtime']
#             print episode['id'],episode['name'],episode['season'],episode['number'],episode['airdate'],episode['airtime'],episode['runtime']
#           return render_template("list_series.html", id=episode['id'], name=episode['name'], season=episode['season'])
#           # and open it to return a handle on the url
#       except urllib2.HTTPError, e:
#         print 'We failed with error code - %s.' % e.code
    # return render_template("list_series.html", get_series.episode['id']=episode[id], get_series.episode['name']=episode[name], get_series.episode['season']=episode[season]) 
    # print get_series.episode(['name'])
  # return render_template("list_series.html", series=series, json=json_content)  

@app.route("/search", methods=["GET"])
def display_search():
    return render_template("search.html")

@app.route("/search", methods=["POST"])
def search():
    query = request.form['query']
    shows = db_session.query(Shows.filter(Show.title.ilike("%" + query + "%")).limit(5)).all()
    return render_template("searchresults.html", shows=shows)


#eturn jsonify(errors=form.errors), 400


def convertkeys(dictionary):
    """Recursively converts dictionary keys to strings."""
    if not isinstance(dictionary, dict):
        return dictionary
    return dict((str(k), convertkeys(v)) 
        for k, v in dictionary.items())

def fixtitle(shows):
    for tv_shows in shows:
      newtitle = show.title.decode('utf-8', 'ignore')
      if newtitle != show.title:
          print "wtf media %d (%s)" % (show.id, newtitle)
          show.title = newtitle

    

 
if __name__ == '__main__':
  app.run(debug=True)
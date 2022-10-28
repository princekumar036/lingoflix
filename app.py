from flask import Flask, render_template, request, flash, redirect, session
import requests
import json
from bs4 import BeautifulSoup
import os

# APP CONFIGS
app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = os.urandom(12)

# TMDB API
TMDB_APIKEY = os.environ.get('TMDB_APIKEY')
def discover_titles(type, page=1):
    url = ( f'https://api.themoviedb.org/3/discover/{type}?'
            f'api_key={TMDB_APIKEY}'
            f'&page={page}'
            f'&region={session["watch_region"].lower()}'
            f'&with_original_language={session["target_language"]}' )
    response = requests.get(url)
    return json.loads(response.text)

def get_title_details(type, id):
    url = ( f'https://api.themoviedb.org/3/{type}/{id}?'
            f'api_key={TMDB_APIKEY}'
            f'&append_to_response=watch/providers' )
    response = requests.get(url)
    return json.loads(response.text)

def get_watch_provider(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.content, features="html.parser")
    stream = soup.find("li", attrs={"class": "ott_filter_best_price"})

    provider = stream.find('a')['title']
    link = stream.find('a')['href']
    img = stream.find('img')['src']

    return {'provider':provider, 'link':link, 'img':img}

@app.route("/")
def home():
    session.clear()

    # # GET COUNTRY CODE FROM IP TO AUTOMATICALLY SET WATCH REGION
    # ip_response = requests.get('http://ip-api.com/json')
    # ip_region = json.loads(ip_response.text)['countryCode']

    f = open('static/tmdb_watch_regions.json')
    regions = json.load(f)

    f = open('static/tmdb_languages.json')
    languages = json.load(f)

    return render_template('index.html', ip_region='IN', regions=regions, languages=languages)


@app.route('/browse', methods=['GET', 'POST'])
def browse():
    print(session)

    # IF GET METHOD, CHECK IF SESSION EXISTS
    if request.method == 'GET':
        if not session:
            flash('Select your target language')
            return redirect('/')
    
    # IF POST POST, SET SESSION FROM FORM DATA
    if request.method == 'POST':
        session['watch_region'] = request.form.get('watch_region')
        session['target_language'] = request.form.get('target_language')
    
    # GET MOVIES FROM TMDB
    print(discover_titles('movies'))
    movies = discover_titles('movie')['results']

    # GET TV SHOWS FROM TMDB
    tvs = discover_titles('tv')['results']
    
    return render_template('browse.html', movies=movies, tvs=tvs)

@app.route('/movie', methods=['GET', 'POST'])
def movie():
    # IF GET METHOD, CHECK IF SESSION EXISTS
    if request.method == 'GET':
        if not session:
            flash('Select your target language')
            return redirect('/')
    
    # IF POST METHOD, RETURN MORE MOVIES
    if request.method == 'POST':
        page_number = request.form.get('movie-pageNo')
        movies = discover_titles('movie', page_number)['results']
        return movies

    response = discover_titles('movie')
    total_pages = response['total_pages']
    movies = response['results']
    return render_template('movie.html', movies=movies, total_pages=total_pages)

@app.route('/tv', methods=['GET', 'POST'])
def tv():
    # IF GET METHOD, CHECK IF SESSION EXISTS
    if request.method == 'GET':
        if not session:
            flash('Select your target language')
            return redirect('/')
    
    # IF POST METHODS, RETURN MORE TV SHOWS
    if request.method == 'POST':
        page_number = request.form.get('tv-pageNo')
        tvs = discover_titles('tv', page_number)['results']
        return tvs

    response = discover_titles('tv')
    total_pages = response['total_pages']
    tvs = response['results']
    return render_template('tv.html', tvs=tvs, total_pages=total_pages)

@app.route('/movie-details')
def movie_details():

    movie_id = request.args.get('id')
    movie = get_title_details('movie', movie_id)

    if session['watch_region'] in movie['watch/providers']['results']:
        link = movie['watch/providers']['results'][session['watch_region']]['link']
        stream = get_watch_provider(link)
        return render_template('movie-details.html', movie=movie, stream=stream)

    return render_template('movie-details.html', movie=movie)

@app.route('/tv-details')
def tv_details():
    
    tv_id = request.args.get('id')
    tv = get_title_details('tv', tv_id)

    if session['watch_region'] in tv['watch/providers']['results']:
        link = tv['watch/providers']['results'][session['watch_region']]['link']
        stream = get_watch_provider(link)

        return render_template('tv-details.html', tv=tv, stream=stream)
        
    return render_template('tv-details.html', tv=tv)


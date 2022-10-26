from flask import Flask, render_template, request, flash, redirect, session
import requests
import json
from bs4 import BeautifulSoup

app = Flask(__name__, static_url_path='/static')
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = b'_5#y2L"F4Q9z\n\xec]/'

TMBD_APIKEY = 'daa7c37e8875b873c494c4070f234516'
def tmdb_discover(type):
    return (f'https://api.themoviedb.org/3/discover/{type}?'
        f'api_key={TMBD_APIKEY}'
        f'&region={session["watch_region"]}'
        f'&with_original_language={session["target_language"]}'
        f'&with_watch_monetization_types=flatrate|free|ads|rent|buy'
    )


@app.route("/")
def home():
    session.clear()

    # # GET COUNTRY CODE FROM IP
    # ip_response = requests.get('http://ip-api.com/json')
    # ip_region = json.loads(ip_response.text)['countryCode']

    f = open('static/tmdb_watch_regions.json')
    regions = json.load(f)

    f = open('static/tmdb_languages.json')
    languages = json.load(f)

    return render_template('index.html', ip_region='IN', regions=regions, languages=languages)


@app.route('/browse', methods=['GET', 'POST'])
def browse():
    
    if request.method == 'POST':
        session['watch_region'] = request.form.get('watch_region')
        session['target_language'] = request.form.get('target_language')

    if request.method == 'GET':
        if not session:
            flash('Select your target')
            return redirect('/')
    
    response = requests.get(tmdb_discover('movie'))
    movies = json.loads(response.text)['results']

    response = requests.get(tmdb_discover('tv'))
    tvs = json.loads(response.text)['results']
    
    return render_template('browse.html', movies=movies, tvs=tvs)

@app.route('/movie')
def movie():
    return render_template('movie.html')

@app.route('/tv')
def tv():
    return render_template('tv.html')

@app.route('/movie-details')
def movie_details():
    movie_id = request.args.get('id')
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMBD_APIKEY}&append_to_response=watch/providers'
    response = requests.get(url)
    movie = json.loads(response.text)

    if session['watch_region'] in movie['watch/providers']['results']:
        watch_providers_link = movie['watch/providers']['results'][session['watch_region']]['link']
        
        r = requests.get(watch_providers_link)
        soup = BeautifulSoup(r.content, features="html.parser")
        stream = soup.find("li", attrs={"class": "ott_filter_best_price"})
        stream_service = stream.find('a')['title']
        stream_link = stream.find('a')['href']
        stream_imgsrc = stream.find('img')['src']

        return render_template('movie-details.html', movie=movie, stream_service=stream_service, stream_link=stream_link, stream_imgsrc=stream_imgsrc)

    return render_template('movie-details.html', movie=movie)

@app.route('/tv-details')
def tv_details():
    tv_id = request.args.get('id')
    url = f'https://api.themoviedb.org/3/tv/{tv_id}?api_key={TMBD_APIKEY}&append_to_response=watch/providers'
    response = requests.get(url)
    tv = json.loads(response.text)

    if session['watch_region'] in tv['watch/providers']['results']:
        watch_providers_link = tv['watch/providers']['results'][session['watch_region']]['link']
        
        r = requests.get(watch_providers_link)
        soup = BeautifulSoup(r.content, features="html.parser")
        stream = soup.find("li", attrs={"class": "ott_filter_best_price"})
        stream_service = stream.find('a')['title']
        stream_link = stream.find('a')['href']
        stream_imgsrc = stream.find('img')['src']

        return render_template('tv-details.html', tv=tv, stream_service=stream_service, stream_link=stream_link, stream_imgsrc=stream_imgsrc)
        
    return render_template('tv-details.html', tv=tv)
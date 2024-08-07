from dotenv import load_dotenv
from flask import redirect, render_template, request, session
from functools import wraps
from google_images_search import GoogleImagesSearch
from gutenbergpy import textget
import os
from random import choice
import requests

gis = GoogleImagesSearch(os.getenv('google_api_key'), os.getenv('search_engine_cx') )
wotd = potd = {"title": "error"}
load_dotenv()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/signin")
        return f(*args, **kwargs)

    return decorated_function

def fetch_word(word):

    if not word:
        return None, None, None, None
    
    url = "https://twinword-word-graph-dictionary.p.rapidapi.com/definition/?entry=" + word
    url_diff = "https://twinword-word-graph-dictionary.p.rapidapi.com/difficulty/?entry=" + word
    header = {"x-rapidapi-key": os.getenv('rapidapi_key'),
              "x-rapidapi-host": "twinword-word-graph-dictionary.p.rapidapi.com"}
    
    response = requests.get(url, headers=header).json()
    difficulty = requests.get(url_diff, headers=header).json().get("ten_degree", "NA")

    api = 'tw'
    error = False

    if response["result_code"] != '200':
        response = fetch_def(word)
        api = 'dapi'
        if "title" in response:
            error = True

    return response, api, error, difficulty

def fetch_def(word):
    url = "https://api.dictionaryapi.dev/api/v2/entries/en/" + word
    response = requests.get(url).json()

    if "title" in response:
        return response
    else:
        return response[0]

def fetch_book_data(title):
    gutindex = open("static/gutindex.txt", "r", encoding="utf-8", errors="ignore")
    index = gutindex.read().find(title)
    gutindex.seek(0)

    if index == -1:
         return "title not found"
    
    name = ''
    consec_space = 0
    in_id = False
    
    for char in gutindex.read()[index:]:
        if char.isnumeric() and consec_space > 1:
             book_id = char
             in_id = True
             
        if char.isnumeric() and in_id and consec_space <= 1:
             book_id += char
        
        if in_id and not char.isnumeric():
             break
        
        name += char
        if char == ' ':
            consec_space += 1
        else:
             consec_space = 0

    return book_id, name.rstrip(" 0123456789")

def fetch_book(title):
    id = fetch_book_data(title)[0]
    name = fetch_book_data(title)[1]

    raw_book = textget.get_text_by_id(id)
    clean_book = textget.strip_headers(raw_book)

    return name, clean_book.split()

def img_search(query):
    image_name = f"{query}.jpg"
    image_path = 'static/covers/' + image_name
    if os.path.exists(image_path):
        return None
    
    search_params = {'q': query + "book cover", 'num': 1, 'fileType': 'jpg', 
                      'rights': 'cc_publicdomain|cc_attribute|cc_sharealike|cc_noncommercial|cc_nonderived'}
    gis.search(search_params=search_params, path_to_dir='static/covers/')

    for image in gis.results():
        downloaded_image_path = image.path    
        os.rename(downloaded_image_path, image_path)

def daily():
    global wotd, potd

    with open('static/large_dictionary.txt', 'r') as file:
        words = file.read().splitlines()
    with open('static/phrases.txt', 'r') as file:
        phrases = file.read().splitlines()

    while True:
        word = choice(words)
        wotd = fetch_def(word)

        if "title" not in wotd:
            break

    while True:
        phrase = choice(phrases)
        potd = fetch_def(phrase)

        if "title" not in potd:
            break
        
    print("daily done")

def fetch_daily():
    return wotd, potd

def rem_punc(string):
    for punctuation in ["\\n","\\r", "!", "?", ".", "'", ",", "~"]:
        if isinstance(string, bytes): 
            string = string.decode('utf-8')

        string = string.replace(punctuation, '')
    return string

def splitlines(string):
    return string.splitlines()

def refine(string):
    for part_of_speech in ["(nou) ", "(vrb) ", "(adj) ", "(adv) "]:
        string = string.replace(part_of_speech, '')
    return string

def add_to_set(set, element):
     set.add(element)
     return set

import os
import sys
import requests
import urllib.parse
import freesound

from flask import redirect, render_template, request, session
from functools import wraps


api_key = os.environ.get("API_KEY")


# setup freesound client
client = freesound.FreesoundClient()
client.set_token(api_key, "token")

def apology(message, code=400):
    """Render message as an apology to user."""
    return render_template("apology.html", top=code, bottom=message), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def synonyms(word):
    """returns dict of 5 most similar words (index 0-4)"""

    # dict format: {0: 'junkie', 1: 'drug+addict', ...}

    try:
        response = requests.get(f"https://api.datamuse.com/words?ml={word}")
        response.raise_for_status()
    except requests.RequestException:
        return None

    try:
        synonyms = response.json()
        words = {}
        words.update({5:word})

        for _ in range(4):
            if ' ' in synonyms[_]["word"]:
                synonyms[_]["word"] = synonyms[_]["word"].replace(' ', '+')
            words[_] = synonyms[_]["word"]
            words[_].replace('\n', ' ')
        return words
    except (KeyError, TypeError, ValueError):
        return None


def formatted(synonyms):
    """ returns string that only contains words from dict, separated by spaces"""
    string = ""
    for word in synonyms.values():
        string += word + ' '
    return string


def replace_space(word):
    """replaces spaces in given word"""
    word.replace(' ', '+')
    return word

def get_results(synonym_list,result_count):
    """returns list of sound id's for a given synonym list and a given result count (5, 10, or 15)"""
    i = 0
    id_list = []
    for word in synonym_list.split():
        print(word)
        results = client.text_search(query=word, fields="id")
        for sound in results:
            # retrieve id of sound, append to list
            id_list.append(sound.id)
            i+=1
            print(sound.id)
            if i == result_count or sound.id == results[-1].id:
                i = 0
                break
    print(id_list)
    return id_list

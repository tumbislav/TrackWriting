# encoding: utf-8
# author: Marko Čibej
# file: paths.py
"""
Temporary collection of Flask-related stuff. To be refactored.
"""

import json
from view import app
from flask import render_template, request

statuses = ['done', 'abandoned', 'idea', 'outline', 'needs review', 'writing', 'reviewing', 'on hold']

works = [
    {'work': 'Blog drafts', 'world': '', 'series': '', 'genre': '',
     'type': 'blog', 'status': 'abandoned', 'count': '1610'},
    {'work': 'Blog posts', 'world': '', 'series': '', 'genre': '',
     'type': 'blog', 'status': 'abandoned', 'count': ''},
    {'work': 'Magical Creatures', 'world': 'Fantasy', 'series': '', 'genre': 'Fantasy',
     'type': 'short story', 'status': 'done', 'count': '3721'},
    {'work': 'The Ontologist', 'world': 'Fantasy', 'series': '', 'genre': 'Science Fiction',
     'type': 'short story', 'status': 'done', 'count': '1325'},
    {'work': 'Verena', 'world': 'Real', 'series': 'Cilly', 'genre': 'Erotica',
     'type': 'short story', 'status': 'done', 'count': '7785'},
    {'work': 'A Bramble of Roses', 'world': 'Real', 'series': 'Fairy Tails', 'genre': 'Erotica',
     'type': 'novelette', 'status': 'done', 'count': '10683'},
    {'work': 'Hood and Wolf', 'world': 'Real', 'series': 'Fairy Tails', 'genre': 'Erotica',
     'type': 'novelette', 'status': 'done', 'count': '14990'},
    {'work': 'Rainfall', 'world': 'Real', 'series': 'The Veil', 'genre': 'Fantasy',
     'type': 'short story', 'status': 'done', 'count': '3138'},
    {'work': 'Know-it-all', 'world': 'Real', 'series': '', 'genre': 'Erotica',
     'type': 'short story', 'status': 'done', 'count': '5852'},
    {'work': 'Stars Think Slow Thought', 'world': 'Cosmos', 'series': '', 'genre': 'Science Fiction',
     'type': 'short story', 'status': 'idea', 'count': ''},
    {'work': 'The Wasp', 'world': 'Exiles', 'series': '', 'genre': 'Science Fiction',
     'type': 'short story', 'status': 'idea', 'count': '198'},
    {'work': 'Sir Tumbalot of the Nile', 'world': 'Fantasy', 'series': 'Tumbalot', 'genre': 'Children\'s',
     'type': 'childrens book', 'status': 'idea', 'count': ''},
    {'work': 'Tales of Gorm the Traveller', 'world': 'Moka', 'series': 'Gorm', 'genre': 'Fantasy',
     'type': 'novel', 'status': 'idea', 'count': ''},
    {'work': 'The City of Bells', 'world': 'Moka', 'series': 'Gorm', 'genre': 'Fantasy',
     'type': 'novel', 'status': 'idea', 'count': ''},
    {'work': 'Yitar', 'world': 'Moka', 'series': 'Gorm', 'genre': 'Fantasy',
     'type': 'novel', 'status': 'idea', 'count': ''},
    {'work': 'Moon\'s farewell', 'world': 'Moka', 'series': 'Serka Tan fe Hun', 'genre': 'Fantasy',
     'type': 'short story', 'status': 'idea', 'count': '70'},
    {'work': 'Wolves of Hun', 'world': 'Moka', 'series': 'Sirvani', 'genre': 'Fantasy',
     'type': 'novel', 'status': 'idea', 'count': ''},
    {'work': 'A Boat Ride', 'world': 'Moka', 'series': '', 'genre': 'Erotica',
     'type': 'short story', 'status': 'idea', 'count': ''},
    {'work': 'Tehcho', 'world': 'Moka', 'series': '', 'genre': 'Fantasy',
     'type': 'short story', 'status': 'idea', 'count': '829'},
    {'work': 'The Raven, the Fox and the Viper', 'world': 'Moka', 'series': '', 'genre': 'Fantasy',
     'type': 'short story', 'status': 'idea', 'count': '85'},
    {'work': 'Seven Kids in a Cottage', 'world': 'Real', 'series': 'Fairy Tails', 'genre': 'Erotica',
     'type': 'short story', 'status': 'idea', 'count': ''},
    {'work': 'Croquis', 'world': 'Real', 'series': 'Immortals', 'genre': 'Erotica',
     'type': 'short story', 'status': 'idea', 'count': '104'},
    {'work': 'The Hearth', 'world': 'Real', 'series': '', 'genre': 'General',
     'type': 'short story', 'status': 'idea', 'count': ''},
    {'work': 'Butterfly', 'world': 'Moka', 'series': 'Sirvani', 'genre': 'Fantasy',
     'type': 'short story', 'status': 'outline', 'count': '379'},
    {'work': 'Of Tarak and Galaia', 'world': 'Moka', 'series': 'Sirvani', 'genre': 'Fantasy',
     'type': 'novelette', 'status': 'outline', 'count': '755'},
    {'work': 'Swordfish Banner', 'world': 'Moka', 'series': 'Sirvani', 'genre': 'Fantasy',
     'type': 'novel', 'status': 'outline', 'count': ''},
    {'work': 'Counterpoint', 'world': 'Cosmos', 'series': '', 'genre': 'Science Fiction',
     'type': 'novel', 'status': 'on hold', 'count': '1616'},
    {'work': 'Exiles outline', 'world': 'Exiles', 'series': '', 'genre': 'Science Fiction',
     'type': 'world building', 'status': 'on hold', 'count': '1287'},
    {'work': 'The Steeling of Dha Ri', 'world': 'Moka', 'series': 'Dha Ri', 'genre': 'Fantasy',
     'type': 'novel', 'status': 'on hold', 'count': '904'},
    {'work': 'Windwagons', 'world': 'Moka', 'series': 'Sirvani', 'genre': 'Fantasy',
     'type': 'novel', 'status': 'on hold', 'count': '9806'},
    {'work': 'Character Sketches', 'world': 'Moka', 'series': '', 'genre': 'General',
     'type': 'world building', 'status': 'on hold', 'count': '16738'},
    {'work': 'Encyclopaedia Bedaica', 'world': 'Moka', 'series': '', 'genre': 'Fantasy',
     'type': 'world building', 'status': 'on hold', 'count': '5147'},
    {'work': 'Geography', 'world': 'Moka', 'series': '', 'genre': 'General',
     'type': 'world building', 'status': 'on hold', 'count': '5959'},
    {'work': 'Peoples and places', 'world': 'Moka', 'series': '', 'genre': 'General',
     'type': 'world building', 'status': 'on hold', 'count': '12135'},
    {'work': 'Ri Language', 'world': 'Moka', 'series': '', 'genre': 'Fantasy',
     'type': 'world building', 'status': 'on hold', 'count': '4870'},
    {'work': 'Second council of Roqo', 'world': 'Moka', 'series': '', 'genre': 'Fantasy',
     'type': 'novel', 'status': 'on hold', 'count': '1514'},
    {'work': 'Emily Tries, But Misunderstands', 'world': 'Near future', 'series': 'Cyber', 'genre': 'Science Fiction',
     'type': 'short story', 'status': 'on hold', 'count': '306'},
    {'work': 'Liz', 'world': 'Real', 'series': 'Cilly', 'genre': 'Erotica',
     'type': 'short story', 'status': 'on hold', 'count': '624'},
    {'work': 'No Names', 'world': 'Real', 'series': '', 'genre': 'Erotica',
     'type': 'novelette', 'status': 'on hold', 'count': '4822'},
    {'work': 'The Mind\'s Rainbow', 'world': 'Real', 'series': '', 'genre': 'Science Fiction',
     'type': 'short story', 'status': 'on hold', 'count': '724'},
    {'work': 'Golden', 'world': 'Moka', 'series': 'Serka Tan fe Hun', 'genre': 'Fantasy',
     'type': 'short story', 'status': 'needs review', 'count': '4400'},
    {'work': 'Harubiri', 'world': 'Moka', 'series': 'Sirvani', 'genre': 'Fantasy',
     'type': 'novel', 'status': 'needs review', 'count': '118677'},
    {'work': 'Kalla', 'world': 'Pleistocene', 'series': 'Hunter', 'genre': 'Erotica',
     'type': 'short story', 'status': 'needs review', 'count': '3435'},
    {'work': 'Little Bird', 'world': 'Pleistocene', 'series': 'Hunter', 'genre': 'Erotica',
     'type': 'short story', 'status': 'needs review', 'count': '4280'},
    {'work': 'Poorman High', 'world': 'Moka', 'series': 'Sirvani', 'genre': 'Fantasy',
     'type': 'short story', 'status': 'writing', 'count': '1477'},
    {'work': 'Teni the Chough', 'world': 'Moka', 'series': 'Sirvani', 'genre': 'Fantasy',
     'type': 'novelette', 'status': 'writing', 'count': '6925'},
    {'work': 'Lullaby', 'world': 'Near future', 'series': 'Cyber', 'genre': 'Science Fiction',
     'type': 'short story', 'status': 'writing', 'count': '2879'},
    {'work': 'Special Accounts', 'world': 'Real', 'series': 'Special accounts', 'genre': 'Erotica',
     'type': 'novel', 'status': 'writing', 'count': '23436'},
    {'work': 'Oliver Midgley\'s Girls', 'world': 'Real', 'series': '', 'genre': 'Erotica',
     'type': 'novelette', 'status': 'writing', 'count': '10861'},
    {'work': 'The Maid Who Climbed Into the Cupboard', 'world': 'Real', 'series': '', 'genre': 'General',
     'type': 'short story', 'status': 'writing', 'count': '1271'},
    {'work': 'A Boy and his sansklat', 'world': 'Cosmos', 'series': '', 'genre': 'Science Fiction',
     'type': 'novelette', 'status': 'writing', 'count': '503'}
]


@app.route('/')
def start_page():
    return render_template('index.html', works=works)


@app.route('/diary', methods=['GET', 'POST'])
def update_diary():
    if request.method == 'GET':
        return json.dumps([{'title': w['title'], 'count': w['count'], 'new-count': 0} for w in works]), 200, \
                {'ContentType': 'application/json'}
    elif request.method == 'POST':
        return json.dumps({'change': request.json['count']}), 200, {'ContentType': 'application/json'}


@app.route('/classifiers/<classifier_set>', methods=['GET'])
def update_classifiers(classifier_set):
    if classifier_set == 'types':
        return json.dumps(statuses), 200, {'ContentType': 'application/json'}
    else:
        pass

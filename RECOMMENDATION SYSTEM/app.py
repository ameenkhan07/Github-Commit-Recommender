from flask import Flask, request, render_template, g
import requests
import sqlite3
import json
from contextlib import closing

# configuration
ACCESS_TOKEN = open('access_token.txt', 'r').read()
DATABASE = '/tmp/recommend.db'
USERNAME = 'admin'
PASSWORD = 'default'

#-------------------- DATABASE SETUP --------------------#


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

#--------------------------------------------------------#

def createJson(url_listy):
    d = []
    outfile = open("COMMIT_SAMPLE.json", "w")
    for i in url_listy:
        response = requests.get(i).json()
        d.append(response["files"])
    json.dump(d, outfile, indent=2)


def reco():
    i = 0
    reco = ""
    rule_split = []
    reco_listy = []
    with open("COMMIT_SAMPLE.json") as f:
        data = json.load(f)
    f.close()

    while(i < len(data[0])):

        file = data[0][i]['filename']
        searchfile = open("rules.txt", "r")

        for line in searchfile:

            rule_split = line.split('==>', 1)
            if (rule_split[0].find(file)) != -1:
                reco = reco+line

        reco_listy.append(reco)
        searchfile.close()
        i = i + 1
    return reco_listy


def commitUrl(sha, url):
    '''
    CREATES A LEGIT API URL FROM THE GIVEN VARIED SOURCED URL
    '''
    url = url.rsplit('/', 2)[0]
    url = url + '/commits/' + str(sha) + '?access_token='+ACCESS_TOKEN
    return url



app = Flask(__name__)
app.config.from_object(__name__)


@app.before_request
def before_request():
    g.db = connect_db()


@app.route('/index')
def index():
    # return 'Index Page'
    db = get_db()
    cur = db.execute('select recommend,timestamp,commit_sha,commit_message, username, repo_url from recommendation order by timestamp desc')
    entries = [dict(recommend=row[0], timestamp=row[1], commit_sha=row[2], commit_message=row[3],username=row[4],repo_url=row[5]) for row in cur.fetchall()]
    repo_url=entries[0]["repo_url"]

    response = requests.get(repo_url+'?access_token='+ACCESS_TOKEN).json()
    # print repo_url
    return render_template('dashboard.html', entries=entries, stars=response['source']['stargazers_count'],forks=response['source']['forks_count'], open_issues=response['source']['open_issues_count'],watchers=response['source']['watchers_count'],repo_name=response['name'])


@app.route("/",  methods=['POST'])
def payload():
    data = json.loads(request.data)
    url_listy = []
    timestamp_listy = []
    commit_url_listy = []
    message_listy = []
    for i in data['commits']:
        api_Url = commitUrl(i['id'], data['repository']['commits_url'])
        commit_url_listy.append(i['url'])
        timestamp_listy.append(i['timestamp'])
        message_listy.append(i['message'])
        url_listy.append(api_Url)

    # print commit_url_listy
    repo_url =  api_Url.rsplit('/', 2)[0]
    print repo_url
    createJson(url_listy)
    reco_listy = reco()
    db = get_db()

    for (c,t,m,r) in zip(commit_url_listy,timestamp_listy,message_listy,reco_listy):
        db.execute('insert into recommendation (recommend,timestamp,commit_sha,commit_message, username, repo_url) values (?,?,?,?,?,?)',[r,t,c,m,data['pusher']['name'],repo_url])
        db.commit()


    return "OK"

if __name__ == '__main__':
    app.debug = True
    app.run()

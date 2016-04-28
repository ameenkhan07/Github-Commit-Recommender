import urllib2
import requests
import json
import time
import sys

# Generated token by github developer site
ACCESS_TOKEN = open('access_token.txt', 'r').read()
dir = "DATA/"
counter = 0


def create_json(req, data):
    '''
    Generate JSON files, [COMMIT URL , FILES CHANGED]
    Commit listing API, pagination in outer loop, developer.github.com/v3
    '''
    global counter
    for commit in req.json():
        listy = []
        if counter < 4900:
            counter += 1
            print counter

            response = requests.get(commit['url']+'?access_token='+ACCESS_TOKEN).json()

            if not bool(response):
                Printer(data)

            # listy.append(response["files"])
            data.append(response["files"])
        else:
            Printer(data, outfile)
    return

def Printer(data, outfile):
        # outfile.write(str(data) + "\n")
        json.dump(data,outfile,indent=2)
        sys.exit(0)


def get_repositories():
    '''
    List the top 30 starred Gituhb repositories repositories
    Search API , developer.github.com/v3
    '''
    list = []
    API = "https://api.github.com/search/repositories?p=1&q=stars%3A>1&s=stars&type=Repositories"
    req = requests.get(API).json()
    # print req
    count = 0
    for i in req['items']:
        count += 1
        s = ''
        for x in i['commits_url'].encode('utf-8'):
            # print x
            if x == '{':
                break
            else:
                s += str(x)
        # print s
        list.append(s)
    return list

API_LIST = get_repositories()
file = 1
# for API in API_LIST:
API = API_LIST[1]
OUT = dir+str(file)+".json"
outfile = open(OUT, "w")
count = 1 #Pagination
data = []
flag = 0
API = API + "?access_token="+ACCESS_TOKEN+"&page="
while True:  # PAGINATION
    url = API + str(count)
    print(url)
    if flag == 1:
        break
    if counter < 4900:
        counter += 1
        req = requests.get(url)

        if not(bool(req.json())):  # All commits listed
            Printer(data, outfile)

        print req.status_code  # Testing
        create_json(req, data)
        print "COUNT" + str(count)
        # pickle.dump(data, outfile)
        count += 1
    else:
            Printer(data, outfile)

        # time.sleep(4000)
        # print counter
        # counter = 0
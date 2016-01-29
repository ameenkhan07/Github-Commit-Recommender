import urllib2
import requests
import json

ACCESS_TOKEN= open('access_token.txt','r').read() #Generated token by github developer site
dir = "DATA/"

def create_json(req,file):
    '''
    Generate JSON files, [COMMIT URL , FILES CHANGED]
    Commit listing API, pagination in outer loop, developer.github.com/v3 
    '''
    pop_list = ["files","url"]
    OUT = dir+str(file)+".json"
    outfile = open(OUT,"a")
    for commit in req.json():
        response = requests.get(commit['url']+'?access_token='+ACCESS_TOKEN).json()
        for key in response.keys():
            if key not in pop_list:
                response.pop(key,None)
        json.dump(response,outfile,indent=2)
    return

def get_repositories():
    '''
    List the top 30 starred Gituhb repositories repositories
    Search API , developer.github.com/v3
    '''
    list=[]
    API = "https://api.github.com/search/repositories?p=1&q=stars%3A>1&s=stars&type=Repositories"
    req = requests.get(API).json()
    count = 0
    for i in req['items']:
        count+=1
        s=''
        for x in i['commits_url'].encode('utf-8'):
            if x ==  '{' :
                break
            else:
                s+=str(x)

        list.append(s)
    return list

API_LIST = get_repositories()
file=0
for API in API_LIST:
    count=1
    file+=1
    API = API + "?access_token="+ACCESS_TOKEN+"&page="
    while True:#PAGINATION
        url=API + str(count)
        print(url)
        req = requests.get(url)
        if not bool(req.json()):
            break
        print req.status_code #Testing
        create_json(req,file)
        count += 1
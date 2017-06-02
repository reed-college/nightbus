### This python script was made by following instructions that can be found at http://nodotcom.org/python-facebook-tutorial.html. They are very detailed and concises so anyone can recreate
### the script. I was able to post to a test facebook page that I made using this script. The only problem is the access_token provided by facebook becomes invalid after a few minutes so that
### needs to be changed everytime. They have an alternative called long access token that can last for 60 days but I don't know how reasonable that time span is. Maybe we can start looking into
### a more permanent solution as we move forward.

import facebook

def main(message):
    cfg = {
            "page_id": 132893597268288,
            
            "access_token": "EAAUg264tb5wBADKZA3dn8x1TUaFWIGGG2ouCOfAfERxnOajfZBaplk2Ivnv2TZATNqd1oCMYNohhwoVzmhN9VZAykP3nfhxQ9xKhQXc2ncdr8qcYwpWrHHZBcQZB2WZBU4OiaBZCZAgHehUhKK3r1sdHybT3tN8E68loZD"
        }

    api = get_api(cfg)
    msg = message
    status = api.put_wall_post(msg)

def get_api(cfg):
    graph = facebook.GraphAPI(cfg['access_token'])
    resp = graph.get_object('me/accounts')
    for page in resp['data']:
         page_access_token = page['access_token']
    graph = facebook.GraphAPI(page_access_token)
    return graph

if __name__ == "__main__":
        main("Hello, I'm a python script that can post to facebook AND I NEVER EXPIRE!!")

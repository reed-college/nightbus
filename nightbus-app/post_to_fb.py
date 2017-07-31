
import facebook
import requests

proxies = {
    "http":"http://tinyproxy.reed.edu:8888/",
    "https": "https://tinyproxy.reed.edu:8888/"
}
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
    graph = facebook.GraphAPI(page_access_token, proxies=proxies)
    return graph

if __name__ == "__main__":
    main()

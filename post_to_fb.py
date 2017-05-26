

import facebook

def main(message):
    cfg = {
            "page_id": 132893597268288,
            "access_token": "EAACEdEose0cBALCAwGTqbpqCyRlyqeKVoywCJlDvlpnwurI5JH5Ct7KnwcIvT9BGDNqHjyN28EMXyRBUCbZCoxZBnKKuothJzOem70kwakZBbZAT8bCF0pp3K7cXPYjFgjbnMUHslqDZCo4sz9lbp4q2dIZCY9tLdiedwtAZCDx3b6X60bUi4p7LyHmgvlXeo0ZD"
        }

    api = get_api(cfg)
    msg = message
    status = api.put_wall_post(msg)

def get_api(cfg):
    graph = facebook.GraphAPI(cfg['access_token'])
    # Get page token to post as the page. You can skip 
    # the following if you want to post as yourself. 
    resp = graph.get_object('me/accounts')
    for page in resp['data']:
        print(page)
        #   if page['id'] == cfg['page_id']:
      #      print(page)
       #     print(page['id'])

           # page_access_token = page['access_token']
    graph = facebook.GraphAPI(page_access_token)
    return graph

if __name__ == "__main__":
        main("Hello, I'm a python script that can post to facebook")

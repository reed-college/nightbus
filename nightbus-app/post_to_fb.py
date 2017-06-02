import facebook

def main(message):
    cfg = {
        "page_id": 132893597268288,
        "access_token": "EAARyarxPwBgBAEVhCid6tCDR3D2FC1fZADDag9gaG2hpEkPWzehnqAF4X2lL7nh158630euzeytIxvP2UE72TZBPLgkRJEhBYrELyXdBA92qO1eU4mnTn0bK0Ykb6WJMLwroDUy9jTGZB3DFGeUR9rWFtIx6J4ZD"
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
        main("Hey it's me Hien!")

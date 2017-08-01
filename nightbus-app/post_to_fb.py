
import facebook
import local_config

proxies = {
    "http": local_config.HTTP_PROXY,
    "https": local_config.HTTPS_PROXY
}

def main(message):
    cfg = {
        "page_id": local_config.FACEBOOK_PAGE_ID,
        "access_token": local_config.FACEBOOK_ACCESS_TOKEN
    }
    api = get_api(cfg)
    msg = message
    status = api.put_wall_post(msg)

def get_api(cfg):
    graph = facebook.GraphAPI(cfg['access_token'])
    resp = graph.get_object('me/accounts')
    for page in resp['data']:
        page_access_token = page['access_token']
    graph = facebook.GraphAPI(access_token=page_access_token, proxies=proxies)
    return graph

if __name__ == "__main__":
    main()

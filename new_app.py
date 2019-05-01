import requests
import base64

CONSUMER_KEY='T6onfLir523hNtBPHJtoDiiss'
CONSUMER_SECRET='to4sK1Slmb0D7kKUyxCDut4jJwSVJPbU8pElOgZB3v4LNVcAVi'

def get_token(CONSUMER_KEY, CONSUMER_SECRET):
    """Used for basic twitter app authentication.

    """
    key_secret = '{}:{}'.format(CONSUMER_KEY, CONSUMER_SECRET).encode('ascii')
    b64_encoded_key = base64.b64encode(key_secret)
    b64_encoded_key = b64_encoded_key.decode('ascii')
    return b64_encoded_key
    
# Getting Access to Twitter API

base_url = 'https://api.twitter.com/'
auth_url = '{}oauth2/token'.format(base_url)
token = get_token(CONSUMER_KEY, CONSUMER_SECRET)

auth_headers = {
    'Authorization': 'Basic {}'.format(token),
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
}
auth_data = {
    'grant_type': 'client_credentials'
}

auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)
access_token = auth_resp.json()['access_token'] 


# Making the Query
search_headers = {
    'Authorization': 'Bearer {}'.format(access_token)    
}

search_params = {
    'q': 'Democrat',
    'count': 10
}

search_url = '{}1.1/users/lookup.json'.format(base_url)
search_resp = requests.get(search_url, headers=search_headers, params=search_params)
tweet_data = search_resp.json()

for x in tweet_data['user']:
    print(x['text'] + '\n')
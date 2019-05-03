import requests
import json
from requests_oauthlib import OAuth1
from utility.signature import create_parameter_string, create_signature_base, get_signing_key, percent_encode
from utility.authentication import create_header_parameters, collect_parameters
from utility.tweet import Tweet


class API(object):
    def __init__(self,
                 consumer_key=None,
                 consumer_secret=None,
                 access_token_key=None,
                 access_token_secret=None):
        """Instantiate a new twitter.Api object.

        Args:
          consumer_key (str):
            Twitter user's consumer_key.
          consumer_secret (str):
            Twitter user's consumer_secret.
          access_token_key (str):
            OAuth access token key value.
          access_token_secret (str):
            OAuth access token's secret.
        """
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token_key = access_token_key
        self.access_token_secret = access_token_secret
        #To be replaced by Auth Session in the future.
        self.auth = OAuth1(self.consumer_key, self.consumer_secret, self.access_token_key, self.access_token_secret, signature_type='auth_header')


def build_URL(base, dic):
    URL = base + "?"
    for k,v in dic.items():
        URL += percent_encode(str(k)) + "=" + percent_encode(str(v)) + "&"
    URL = URL[:-1]
    return URL

# Need to fix logic in this def
def organize_locals(param_dict):
    bool_dict = {True: 'true', False: 'false'}
    par = {}
    args = {}
    kwargs = {}
    for x,y in param_dict.items():
        # Used for determining if this is an args parameter
        if type(y) is tuple:
            values = ""
            for v in y:
                if type(v) is bool:
                    values += bool_dict[v]  + ","
                else:
                    values += str(v) + ","
            values = values[:-1]
            args[x] = y
        # Used for determining if this is a kwargs parameter
        elif type(y) is dict:
            for k,v in y.items():
                if type(v) is bool:
                    v = bool_dict[v]
                else:
                    y[k] = str(v)
            kwargs = y
        # Used for determining any other parameter
        else:
            if type(y) is bool:
                y = bool_dict[y]
            else:
                y = str(y)
            par[x] = y
    organized_parameters = {**par, **args, **kwargs}
    return organized_parameters


# Get user object from screen_name or id
def get_users_lookup(screen_name, include_entities=False, tweet_mode=False):
    """ Returns fully-hydrated user objects for up to 100 users per request, as specified by comma-separated values passed to the user_id and/or screen_name parameters.

        This method is especially useful when used in conjunction with collections of user IDs returned from GET friends / ids and GET followers / ids.

        GET users / show is used to retrieve a single user object.

        There are a few things to note when using this method.

        You must be following a protected user to be able to see their most recent status update. If you don't follow a protected user their status will be removed.
        The order of user IDs or screen names may not match the order of users in the returned array.
        If a requested user is unknown, suspended, or deleted, then that user will not be returned in the results list.
        If none of your lookup criteria can be satisfied by returning a user object, a HTTP 404 will be thrown.
        You are strongly encouraged to use a POST for larger requests.

        user: A comma separated list of user IDs or screen names (as specified by the screen_names parameter), up to 100 are allowed in a single request. You are strongly encouraged to use a POST for larger requests.
        
        screen_name: A comma separated list of screen names, up to 100 are allowed in a single request. You are strongly encouraged to use a POST for larger (up to 100 screen names) requests.
        
        include_entities: The entities node that may appear within embedded statuses will not be included when set to false.
        
        tweet_mode	optional: Valid request values are compat and extended, which give compatibility mode and extended mode, respectively for Tweets that contain over 140 characters
    """
    saved_args = organize_locals(dict(locals()))
    HTTP_method = "GET"
    base_URL = "https://api.twitter.com/1.1/users/lookup.json"

    oauth_dict = collect_parameters(saved_args)
    parameter_string = create_parameter_string(oauth_dict)
    signature_base = create_signature_base(HTTP_method, base_URL, parameter_string)
    oauth_signature = get_signing_key(signature_base)

    # Sending the request
    headers = create_header_parameters(oauth_dict, oauth_signature)
    new_URL = build_URL(base_URL, saved_args)
    r = requests.get(new_URL, headers=headers)
    return r


def get_users_search(q, page=1, count=20, include_entities=False):
    """ Provides a simple, relevance-based search interface to public user accounts on Twitter. Try querying by topical interest, full name, company name, location, or other criteria. Exact match searches are not supported.

        Only the first 1,000 matching results are available.

        Args:
            q: 
                The search query to run against people search.
            
            page: 
                Specifies the page of results to retrieve.
            
            count: 
                The number of potential user results to retrieve per page. This value has a maximum of 20.
            
            include_entities: 
                The entities node will not be included in embedded Tweet objects when set to false.  
    """
    saved_args = organize_locals(dict(locals()))
    HTTP_method = "GET"
    base_URL = "https://api.twitter.com/1.1/users/search.json"
    
    new_URL = build_URL(base_URL, saved_args)
    r = requests.get(new_URL, auth=API.auth)
    return r


def send_direct_message(user, message):
    """ Publishes a new message_create event resulting in a Direct Message sent to a specified user from the authenticating user. Returns an event if successful. Supports publishing Direct Messages with optional Quick Reply and media attachment. Replaces behavior currently provided by POST direct_messages/new.

        Requires a JSON POST body and Content-Type header to be set to application/json. Setting Content-Length may also be required if it is not automatically.

        user: The user which the message will be sent to.

        message: The message that will be sent.

        #To be added later
        
        quick_reply.type (optional)	
        
        attachment.type (optional)	The attachment type. Can be media or location.
        
        attachment.media.id (optional)
    """

    HTTP_method = "POST"
    base_URL = "https://api.twitter.com/1.1/direct_messages/events/new.json"

    oauth_dict = collect_parameters({})
    parameter_string = create_parameter_string(oauth_dict)
    signature_base = create_signature_base(HTTP_method, base_URL, parameter_string)
    oauth_signature = get_signing_key(signature_base)

    # Sending the request
    payload = {"event": {"type": "message_create", "message_create": {"target": {"recipient_id": "{}".format(user)}, "message_data": {"text": "{}".format(message)}}}}
    headers = create_header_parameters(oauth_dict, oauth_signature, ("content-type", "application/json"))
    r = requests.post(base_URL, data=json.dumps(payload), headers=headers)
    return r


def update_status(status):
    """ Updates the authenticating user's current status, also known as Tweeting.

        For each update attempt, the update text is compared with the authenticating user's recent Tweets. Any attempt that would result in duplication will be blocked, resulting in a 403 error. A user cannot submit the same status twice in a row.

        While not rate limited by the API, a user is limited in the number of Tweets they can create at a time. If the number of updates posted by the user reaches the current allowed limit this method will return an HTTP 403 error.

        status: The text of the status update. URL encode as necessary.
    """
    saved_args = organize_locals(dict(locals()))
    HTTP_method = "POST"
    base_URL = "https://api.twitter.com/1.1/statuses/update.json"

    oauth_dict = collect_parameters(saved_args)
    parameter_string = create_parameter_string(oauth_dict)
    signature_base = create_signature_base(HTTP_method, base_URL, parameter_string)
    oauth_signature = get_signing_key(signature_base)

    # Sending the request
    headers = create_header_parameters(oauth_dict, oauth_signature)
    new_URL = build_URL(base_URL, saved_args)
    r = requests.get(new_URL, headers=headers)
    return r


def get_timeline_user(screen_name, count=200, trim_user=True, exclude_replies=True, include_rts=False, **id_pos):
    """ Returns a collection of the most recent Tweets posted by the user indicated by the screen_name or user_id parameters.

        User timelines belonging to protected users may only be requested when the authenticated user either "owns" the timeline or is an approved follower of the owner.

        The timeline returned is the equivalent of the one seen as a user's profile on Twitter.

        This method can only return up to 3,200 of a user's most recent Tweets. Native retweets of other statuses by the user is included in this total, regardless of whether include_rts is set to false when requesting this resource.

        user: 
        
        screen_name:
        
        count: 
        
        trim_user: 

        exclude_replies:

        inlude_rts:

        max_id: 
        
        since_id:
    """
    saved_args = organize_locals(dict(locals()))
    HTTP_method = "GET"
    base_URL = "https://api.twitter.com/1.1/statuses/user_timeline.json"
    
    oauth_dict = collect_parameters(saved_args, parse=True)
    parameter_string = create_parameter_string(oauth_dict)
    signature_base = create_signature_base(HTTP_method, base_URL, parameter_string)
    oauth_signature = get_signing_key(signature_base)

    # Sending the request
    headers = create_header_parameters(oauth_dict, oauth_signature)
    new_URL = build_URL(base_URL, saved_args)
    r = requests.get(new_URL, headers=headers)
    return r


def print_statuses(username, count=2000):
    request_count = 0
    results = []
    r = get_timeline_user(username, tweet_mode="extended")
    request_count += 1

    if r.status_code is not 200:
        exit()

    for i in r.json():
        results.append(Tweet(i))

    while len(results) < count: 
        r = get_timeline_user(username, tweet_mode="extended", max_id=(results[-1]._id-1))
        request_count += 1
        
        if r.status_code is not 200 or not r.json():
            break
        
        for i in r.json():
            results.append(Tweet(i))

    for i in results:
        print(i.text)

    print(request_count)


r = get_users_search("Bay Area")
print('d')
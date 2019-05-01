import time
from collections import OrderedDict
from utility.secrets import CONSUMER_KEY, ACCESS_TOKEN_KEY
from utility.signature import encode_dict

def generate_nonce(digits=16):
    """
        Generate a unique random string.
    """
    import random, string
    x = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(digits))
    return(x)


def get_time():
    """
        Get current time.
    """
    import time
    return str(int(time.time()))


def collect_parameters(par, parse=False):
    """
        Use to create the signature parameters. If additional parameters are required provide in args.

        (Optional) args: Tuple containing key value pair for additional argument(s).
    """

    # Default parameter dict.
    oauth_dict = {
        'oauth_consumer_key':CONSUMER_KEY,
        'oauth_nonce':generate_nonce(),
        'oauth_signature_method':"HMAC-SHA1",
        'oauth_timestamp':get_time(),
        'oauth_token':ACCESS_TOKEN_KEY,
        'oauth_version':"1.0"
    }

    # Include additional parameters.
    for k,v in par.items():
        oauth_dict[k] = str(v)

    # Sort all items in alphabetical order. Must be percent encoded.
    oauth_dict = encode_dict(oauth_dict)
    oauth_dict = OrderedDict(sorted(oauth_dict.items()))
    return oauth_dict

# Need to fix this to be more dynamic.
def create_header_parameters(oauth_dict, oauth_signature, *args):
    """
        Use to create the header parameters. If additional parameters are required provide in args.

        (Optional) args: Tuple containing key value pair for additional argument(s).
    """
    auth_string = 'OAuth oauth_consumer_key="{}", oauth_nonce="{}", oauth_signature="{}", oauth_signature_method="{}", oauth_timestamp="{}", oauth_token="{}", oauth_version="{}"'.format(
        oauth_dict["oauth_consumer_key"],
        oauth_dict["oauth_nonce"],
        oauth_signature,
        oauth_dict["oauth_signature_method"],
        oauth_dict["oauth_timestamp"],
        oauth_dict["oauth_token"],
        oauth_dict["oauth_version"]
    )

    header_dict = {"authorization": "{}".format(auth_string)}

    # Include additional parameters.
    for arg in args:
        k, v = arg
        header_dict[k] = v

    return header_dict
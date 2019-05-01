from utility.secrets import CONSUMER_SECRET, ACCESS_TOKEN_SECRET

def percent_encode(string, plus=False):
    """
        Percent encode a string.

        string: A string element to be encoded. 
    """
    import urllib
    x = urllib.parse.quote(string, safe='')
    return x


def encode_dict(d):
    """
        Percent encode dict.

        d: Dictionary to be percent encoded.
    """
    new = {}
    for k,v in d.items():
        k = percent_encode(k)
        v = percent_encode(v)
        new[k] = v

    return new


def create_parameter_string(d):
    parameter_string = ""
    for k,v in d.items():
        parameter_string += str(k) + '=' + str(v) + '&'
    parameter_string = parameter_string[:-1]
    return parameter_string


def create_signature_base(method, base_URL, string):
    signature_base = method + '&' + percent_encode(base_URL) + '&' + percent_encode(string)
    return signature_base


def get_signing_key(signature_base_string):
    from hashlib import sha1
    import hmac
    import base64

    signature_key = CONSUMER_SECRET + "&" + ACCESS_TOKEN_SECRET

    raw = signature_base_string.encode("UTF-8")
    key = signature_key.encode("UTF-8") 
    hashed = hmac.new(key, raw, sha1)
    
    # The signature
    oauth_signature = base64.b64encode(hashed.digest()).decode("UTF-8")
    return percent_encode(oauth_signature)
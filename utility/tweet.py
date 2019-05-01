class Tweet():
    #will fix to fit all cases
    def __init__(self, json):
        self.created_at = json['created_at']
        self._id = json['id']
        self._id_str = json['id_str']
        try:
            self.text = json['text'] 
        except:
            self.text = json['full_text']
        self.truncated = json['truncated']
        self.entities = json['entities']
        self.source = json['source']
        self.in_reply_to_status_id = json['in_reply_to_status_id']
        self.in_reply_to_status_id_str = json['in_reply_to_status_id_str']
        self.in_reply_to_user_id = json['in_reply_to_user_id']
        self.in_reply_to_user_id_str = json['in_reply_to_user_id_str']
        self.in_reply_to_screen_name = json['in_reply_to_screen_name']
        self.user = json['user']
        self.geo = json['geo']
        self.coordinates = json['coordinates']
        self.place = json['place']
        self.contributors = json['contributors']
        self.is_quote_status = json['is_quote_status']
        self.retweet_count = json['retweet_count']
        self.favorite_count = json['favorite_count']
        self.favorited = json['favorited']
        self.retweeted = json['retweeted']
        self.lang = json['lang']
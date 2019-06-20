DROP TABLE users

CREATE TABLE users (user_id INTEGER PRIMARY KEY, 
screen_name TEXT, 
location TEXT,
description TEXT, 
protected BOOL, 
followers INTEGER,
friends INTEGER, 
created_at TEXT,  
verified BOOL, 
tweets INTEGER,
lang TEXT);

CREATE TABLE tweets (tweet_id INTEGER PRIMARY KEY
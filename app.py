import asyncio
from twitter import Api
import pandas as pd
import json

follow_limit = 400 # per day for user
expiration_time = 60*60*24*2 # 2 days

api = Api(consumer_key="T6onfLir523hNtBPHJtoDiiss",
        consumer_secret="to4sK1Slmb0D7kKUyxCDut4jJwSVJPbU8pElOgZB3v4LNVcAVi",
        access_token_key="2184575798-8O3dX2NECWmUJKanm81C1pj3zC3DjLoniYR0j4Q",
        access_token_secret="gd4gDVf1eWms7qyMMQSwFnOybnojy619gVdiMWHW3R85z")

owner = api.GetUser(screen_name="slyduda").json()


# Two ways to get leads: Followers and raw searches

followers = set()
following = set()
friendships = set()
queue = []
leads = set()
data = {}


def update_frienships():
        global followers, following, friendships, searched, queue
        # Get an updated list of all followers and add to all previous followers
        response = api.GetFollowerIDs(user_id=owner['id']) ################################# Limited by 15 minutes to 15
        followers = followers.union(response)

        #Get an updated list of all following and add to all previous following
        response = api.GetFriendIDs(user_id=owner['id']) ################################
        following = following.union(response)

        # Get all current friendships and add new ones to the queue
        current_friends = followers.intersection(following)
        new_friends = current_friends.difference(friendships)
        queue.append(new_friends)

        # Update friendships to contain all current friends
        friendships = current_friends

def get_leads():
        global queue, leads, data
        search = queue[:100]
        results = api.UsersLookup(user_id=search) ###############################
        leads = [a['id'] for a in results]
        data = [{a['id']:a} for a in results]
        del queue[:100]


def get_timeline():
        pass


def search_user(term=str):
        """
        Used to search for a new potential lead based on user or ML feedback.

        Args:
                term (string): Use to adjust next auto follow criteria.

        """
        pass

async def auto_follow(_id=None, expiration=expiration_time, keep_follow=True, mute=True):
        """
        Used to automatically follow another user.

        Args:
                expration (int): Time before checking lead response.

                keep_follow (bool): If target follows user, continue to follow.

                mute (bool): Silence all device notifications and retweets from user.
        """
        # Creating the friendship.
        if _id:
                api.CreateFriendship(user_id=_id, follow=False, retweets=False)
        else:
                print("Issue creating friendship.")
                await asyncio.sleep(expiration)
                return
        await asyncio.sleep(expiration)

        # Getting the result from the target.
        result = api.ShowFriendship(owner["id"]).json()
        if keep_follow:
                if result["relationship"]["target"]["following"]:
                        friendships.add(_id)
        else:
                api.DestroyFriendship(user_id=_id)
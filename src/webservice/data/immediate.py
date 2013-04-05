from Twitter.ApiWrapper import Wrapper


wrapper = Wrapper()
tweets = wrapper.Search("Welfare")

for tweet in tweets:
    print tweet

__author__ = 'MichaelI'

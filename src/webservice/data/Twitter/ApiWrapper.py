import twitter
import requests

class Wrapper(object):
    def __init__(self):
        self.consumerKey = 'kEt0VMtLFqa3truyX2HE0w'
        self.consumerSecret = 'Vo59dzgpAH5jFXonX4S7uMqkgEqHlvKyOBBOhKipGI'
        self.accessTokenKey = '14985980-mzT24hBfuWJv0McO61qdgEb0uFuJqKTtpGYRWGqlZ'
        self.accessTokenSecret = 'TEdRBmGgO60luTB6DGXdEow9ZwMO7G4N2Sf1hlUdaCo'
        self.API = None

    def GetAPI(self):
        if self.API is None:
            self.API = twitter.Api(consumer_key='kEt0VMtLFqa3truyX2HE0w', consumer_secret='Vo59dzgpAH5jFXonX4S7uMqkgEqHlvKyOBBOhKipGI', access_token_key='14985980-mzT24hBfuWJv0McO61qdgEb0uFuJqKTtpGYRWGqlZ', access_token_secret='TEdRBmGgO60luTB6DGXdEow9ZwMO7G4N2Sf1hlUdaCo')
        return self.API

    def Search(self, term):
        results = self.GetAPI().GetSearch(term=term, include_entities=True)
        tweets = []
        for result in results:
            tweet = TweetResult()
            tweet.Tweet = result.text
            tweet.Urls = self.ExtractURLs(result, False)
            tweet.ExpandedUrls = self.ExtractURLs(result, True)
            tweet.OriginalUrls = self.ChaseUrls(tweet.ExpandedUrls)
            tweets.append(tweet)
        return tweets

    def ExtractURLs(self, tweet, expanded):
        if tweet.urls is None:
            return ''
        urlStr = ''
        for url in tweet.urls:
            urlStr += url.expanded_url + ', ' if expanded else url.url + ', '
        if len(urlStr) > 1:
            return urlStr[:-2]
        return urlStr

    def ChaseUrls(self, urlStr):
        if len(urlStr) < 5:
            return ''
        urls = urlStr.split(',')
        urlStr = ''
        for url in urls:
            orig = self.GetOriginalUrl(url)
            urlStr += orig + ", "
        if len(urlStr) > 1:
            return urlStr[:-2]
        return urlStr

    def GetOriginalUrl(self, url):
        resp = requests.get(url)
        if resp.status_code == 200:
            return resp.url
        return ''



class TweetResult(object):
    def __init__(self):
        self.Tweet = None
        self.Urls = None
        self.ExpandedUrls = None
        self.OriginalUrls = None

    def __str__(self):
        return self.Tweet + " | " + self.Urls + " | " + self.ExpandedUrls + " | " + self.OriginalUrls

__author__ = 'MichaelI'


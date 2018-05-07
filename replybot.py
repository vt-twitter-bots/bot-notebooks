import tweepy
import time

# Requires the consumer and app secrets to be pasted in for your own application
auth = tweepy.OAuthHandler("", "")
auth.set_access_token("", "")

api = tweepy.API(auth)

# Twitter ID of the bot account - Replace before running
SELF_ID = 000

keySet = set()
isInfinite = False


def handleMessage(tweet, key):
    # printTweet(tweet)
    if isTweetMention(tweet):
        commitLog(key)
        postResponse(tweet)


def postResponse(tweet):
    response = ""
    response += getUserFromRequest(tweet) + " "
    if "learn" in tweet.text:
        response += "Stay in school!"
    elif "help" in tweet.text:
        response += "I'm not smart enough to know the answer!"
    elif "who are you?" in tweet.text:
        response += "I'm a bot helping out with an academic project"
    else:
        response += "I don't know what you're asking me"
    response += " https://twitter.com/" + getUserFromRequest(tweet)[1:] + "/status/" + tweet.id_str
    api.update_status(response)


def commitLog(id):
    keySet.add(id)
    print("COMMIT: " + str(id))


def writeOut():
    with open('log.txt', 'w') as f:
        for key in keySet:
            # print(key)
            f.write("%s\n" % str(key))


def readIn():
    with open('log.txt') as fp:
        for line in fp:
            keySet.add(line.rstrip())
            # print(line.rstrip())


def getTweets():
    public_tweets = api.home_timeline()
    key = ""
    for tweet in public_tweets:
        key = str(tweet.user.id) + "," + str(tweet.id)
        if not keySet.__contains__(key):
            handleMessage(tweet, key)


def isTweetMention(tweet):
    userMentions = tweet._json['entities']['user_mentions']
    # print(userMentions)
    tweetIsMention = False
    for mention in userMentions:
        if mention['id'] == SELF_ID:
            tweetIsMention = True
            #print(mention)
    if tweetIsMention:
        return True
    else:
        return False


def getUserFromRequest(tweet):
    return "@" + str(tweet.user.screen_name)


def printTweet(tweet):
    print(tweet._json)

# api.update_status("test")

for x in range(0,1):
    readIn()
    getTweets()
    writeOut()
    time.sleep(20)
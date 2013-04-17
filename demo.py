import tweepy
import datetime
import urllib
import urllib2
import props

auth = tweepy.OAuthHandler(props.consumer_key, props.consumer_secret)
auth.set_access_token(props.access_token, props.access_token_secret)

#twitter account to monitor
account = "romamobilita"

#topics of interest
topics = ["metro", "scioper"]
hours = 1

api = tweepy.API(auth)

user = api.get_user(account)


# filter tweets of def
def isInteresting(s):
    flag = False
    for topic in topics:
        flag = flag or s.find(topic) >= 0
    return flag


# filter recent tweets
def recent(el):
    c = datetime.datetime.now() - el.created_at
    return c.seconds < 60*(60*hours+5) and isInteresting(el.text.lower())


# send notification using boxcat
def send_notice(site, code):
    api_url = 'http://boxcar.io/devices/providers/%s/notifications' % props.BOXCAR_API_KEY
    print api_url
    data = {
        'email': props.BOXCAR_EMAIL,
        'notification[from_screen_name]': site,
        'notification[message]': code.encode('utf-8')
    }
    print data
    urllib2.urlopen(api_url, urllib.urlencode(data))

for tweet in filter(recent, user.timeline()):
    print "send notification"
    send_notice(account, tweet.text)

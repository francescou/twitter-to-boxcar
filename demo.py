import tweepy
import datetime
import sys, os, urllib, urllib2, hashlib, datetime
import props

auth = tweepy.OAuthHandler(props.consumer_key, props.consumer_secret)
auth.set_access_token(props.access_token, props.access_token_secret)

account = "romamobilita"
topics = ["metro", "scioper"]
hours=1

api = tweepy.API(auth)

user = api.get_user(account)

def isInteresting(s):
  flag = False
  for topic in topics:
    flag = flag or s.find(topic) >= 0
  return flag

def recent(el):
    c = datetime.datetime.now() - el.created_at
    return c.seconds < 60*(60*hours+5) and isInteresting(el.text.lower())

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

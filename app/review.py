from app import app
import pywikibot
from pywikibot import pagegenerators
from pywikibot.bot import ExistingPageBot
from datetime import datetime, timedelta

class Review(ExistingPageBot):
    
    def __init__(self, lang):
        self.site = site = pywikibot.Site(lang, 'wikipedia')
        self.res24 = self.countReviews(datetime.now(), 24)
        self.res168 = self.countReviews(datetime.now(), 168)
        self.res = { "24": sorted(self.res24, key=self.res24.__getitem__, reverse=True),
                    "168": sorted(self.res168, key=self.res168.__getitem__, reverse=True)
                    }


    def countReviews(self,starttime, hours):

        # Dict of tuples (review total, initial, other, unreview)
        reviews = {}
        count = 0
        
        for le in self.site.logevents(end=starttime, start=starttime-timedelta(hours=hours), reverse=True, logtype='review'):
        #for le in self.site.logevents(end=starttime, start=starttime-datetime.timedelta(hours=hours), reverse=True):
            #if le.action().startswith('unapprove'):
            count += 1
            # print('%i>>%s>>%s>>%s>>%s>>%s>>%s' % (count, le.type(), le.logid(),le.timestamp(),le.action(),le.user(),le.page()))
            r = self.addreview(reviews,le.user(),le.action())
            total, initial, other, unreview = r
            if total != 0:
                reviews[le.user()] = r

        #print(reviews)
        return(reviews)

    def addreview(self, dictionary, user, action):
        #tuple (review total, initial, other, unreview)

        if user in dictionary.keys():
            total, initial, other, unreview = dictionary[user]
        else:
            total = 0
            initial = 0 
            other = 0
            unreview = 0
        # print('IN:%s>>%s>>%i>>%i>>%i>>%i' % (action, user, total, initial, other, unreview))
        # distinguish automatic review
        if not action.endswith('a'):
            total += 1
            if action.startswith('unapprove'):
                unreview += 1
            elif '-i' in action:
                initial += 1
            else:
                other += 1
        else:
            print('Skipped automatic review')
            
        # print('OUT:%s>>%s>>%i>>%i>>%i>>%i' % (action, user, total, initial, other, unreview))
        return (total, initial, other, unreview)
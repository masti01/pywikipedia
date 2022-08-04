from app import app
import pywikibot
from pywikibot import pagegenerators
from pywikibot.bot import ExistingPageBot
from datetime import datetime, timedelta

class Deletes(ExistingPageBot):
    
    def __init__(self, lang):
        self.site = site = pywikibot.Site(lang, 'wikipedia')
        self.blocks = { "reasons": self.delete_reasons(datetime.now(), 30),
                       "admins": self.delete_stats(datetime.now(), 30)
                       }


    def delete_reasons(self,starttime, days):

        # Dict of tuples (block reason, number)
        deletes = {}
        sdeletes = []

        #for le in self.site.logevents(end=starttime, start=starttime-datetime.timedelta(days=days), reverse=True, logtype='block'):
        for le in self.site.logevents(start=starttime-timedelta(days=days), end=starttime, reverse=True, logtype='delete'):
            try:
                comment = le.comment()
            except KeyError:
                comment = u''
            if comment in deletes.keys():
                deletes[comment] += 1
            else:
                deletes[comment] = 1
                
        for b in sorted(deletes, key=deletes.__getitem__, reverse=True):
            if deletes[b] > 1:
                sdeletes.append((deletes[b], b))

        return(sdeletes)


    def delete_stats(self,starttime, days):
        #calculate block stats per admin
        print('Analyzing deletes log last %i days.' % days)
        # Dict of tuples (admin, number)
        deletes = {}
        sdeletes = []
        count = 0

        #for le in self.site.logevents(end=starttime, start=starttime-datetime.timedelta(days=days), reverse=True, logtype='block'):
        for le in self.site.logevents(start=starttime-timedelta(days=days), end=starttime, reverse=True, logtype='delete'):
            count += 1
            try:
                if le.user() in deletes.keys():
                    deletes[le.user()] += 1
                else:
                    deletes[le.user()] = 1
            except:
                if u'BŁĄD DANYCH' in deletes.keys():
                    deletes[u'BŁĄD DANYCH'] += 1
                else:
                    deletes[u'BŁĄD DANYCH'] = 1
                continue

        for b in sorted(deletes, key=deletes.__getitem__, reverse=True):
            if deletes[b] > 1:
                percent = deletes[b]/count
                sdeletes.append((b, deletes[b], percent, f'{percent*100:.2f}%'))
                
        print(sdeletes)

        return(sdeletes)
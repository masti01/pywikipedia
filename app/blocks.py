from app import app
import pywikibot
from pywikibot import pagegenerators
from pywikibot.bot import ExistingPageBot
from datetime import datetime, timedelta

class Blocks(ExistingPageBot):
    
    def __init__(self, lang):
        self.site = site = pywikibot.Site(lang, 'wikipedia')
        self.blocks = { "reasons": self.block_reasons(datetime.now(), 30),
                       "admins": self.block_stats(datetime.now(), 30)
                       }


    def block_reasons(self,starttime, days):

        # Dict of tuples (block reason, number)
        blocks = {}
        sblocks = []

        #for le in self.site.logevents(end=starttime, start=starttime-datetime.timedelta(days=days), reverse=True, logtype='block'):
        for le in self.site.blocks(starttime=starttime-timedelta(days=days), endtime=starttime, reverse=True):
            if le['reason'] in blocks.keys():
                blocks[le['reason']] += 1
            else:
                blocks[le['reason']] = 1
                
        for b in sorted(blocks, key=blocks.__getitem__, reverse=True):
            if blocks[b] > 1:
                sblocks.append((blocks[b], b))

        return(sblocks)


    def block_stats(self,starttime, days):
        #calculate block stats per admin
        print('Analyzing block log last %i days.' % days)
        # Dict of tuples (admin, number)
        blocks = {}
        sblocks = []
        count = 0

        #for le in self.site.logevents(end=starttime, start=starttime-datetime.timedelta(days=days), reverse=True, logtype='block'):
        for le in self.site.blocks(starttime=starttime-timedelta(days=days), endtime=starttime, reverse=True):
            count += 1
            if le['by'] in blocks.keys():
                blocks[le['by']] += 1
            else:
                blocks[le['by']] = 1

        for b in sorted(blocks, key=blocks.__getitem__, reverse=True):
            if blocks[b] > 1:
                percent = blocks[b]/count
                sblocks.append((b, blocks[b], percent, f'{percent*100:.2f}%'))
                
        print(sblocks)

        return(sblocks)
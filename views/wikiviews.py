from multiprocessing.sharedctypes import RawValue
from flask import render_template
from app import app
import pywikibot
from app.review import Review
from app.blocks import Blocks
from app.deletes import Deletes

@app.route("/")
def wiki_page():
    site = pywikibot.Site('pl', 'wikipedia')  # The site we want to run our bot on
    page = pywikibot.Page(site, 'Kantar Media Intelligence')
    
    print(page.text)
    return render_template("wiki/index.html", title=page.title(), text=page.text)

@app.route("/review")
@app.route("/redaktorzy")
def wiki_review():
    
    rv = Review('pl')
    
    # print(rv.res)
    return render_template("wiki/review.html", title='Statystyki redaktorów', sort=rv.res, res24=rv.res24, res168=rv.res168)

@app.route("/blocks")
@app.route("/blokady")
def wiki_blocks():
    
    bl = Blocks('pl')
    
    #print(bl.blocks)
    return render_template("wiki/blocks.html", title='Statystyki blokad', blocks=bl.blocks)
    
@app.route("/deletes")
@app.route("/usuwanie")
def wiki_deletes():
    
    bl = Deletes('pl')
    
    #print(bl.blocks)
    return render_template("wiki/blocks.html", title='Statystyki blokad', blocks=bl.blocks)
from flask import Flask

app = Flask('__name__', static_folder='app/static', template_folder='app/templates')

print('APP started')

from app import views
from app import admin_views
from app import wikiviews

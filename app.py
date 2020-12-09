#!/usr/bin/env python

import sys

import pypandoc
import os

from flask import Flask, render_template
from flaskext.markdown import Markdown

from flask_frozen import Freezer

app = Flask(__name__)
Markdown(app)
freezer = Freezer(app)

dirname = os.path.dirname(__file__)

projects = [os.path.splitext(f)[0] for f in os.listdir(os.path.join(dirname, "static/body/projects"))] 
writings = [os.path.splitext(f)[0] for f in os.listdir(os.path.join(dirname, "static/body/writings"))] 

#index
@app.route("/")
def index():
    mkd_text = open("static/body/info/index.md", 'r').read()
    return render_template("page.html", mkd=mkd_text, projects=projects, writings=writings)

#pencils
@app.route("/info/pencils/")
def pencils():
    mkd_text = open("static/body/info/pencils.md", 'r').read()
    return render_template("page.html", mkd=mkd_text, projects=projects, writings=writings)

#contact
@app.route("/info/contact/")
def contact():
    mkd_text = open("static/body/info/contact.md", 'r').read()
    return render_template("page.html", mkd=mkd_text, projects=projects, writings=writings)

#content pages
@app.route("/<string:topLevel>/<path>/")
def page(topLevel, path):
    #this string stuff is bad practice don't do this, use os functions instead eventually
    mkd_text = open("static/body/" + topLevel + "/" + path + ".md", 'r').read()
    return render_template("page.html", mkd=mkd_text, projects=projects, writings=writings)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        app.run(port=8000)

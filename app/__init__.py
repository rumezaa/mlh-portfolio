import os
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', title="MLH Fellow", url=os.getenv("URL"))

@app.route('/hobbies')
def hobbies_page():
    hobbies = [
        {
            'name': 'Soccer',
            'img': 'img/soccer.jpg',
            'alt': 'Soccer ball on a field',
            'desc': "I'm an avid soccer fan and player, enjoying both watching matches and playing in local leagues. It's a great way to stay active, sharpen my strategic thinking, and work as part of a team."
        }
    ]
    return render_template('hobbies.html', title="My Hobbies", hobbies=hobbies)

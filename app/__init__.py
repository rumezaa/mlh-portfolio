import datetime
import json
import os

from dotenv import load_dotenv
from flask import Flask, render_template, request
from peewee import *
from playhouse.shortcuts import model_to_dict

load_dotenv()
app = Flask(__name__)

if os.getenv("TESTING") == "true":
    print("RUNNING IN TEST MODE")
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared&uri=true')
else:
    mydb = MySQLDatabase(
        os.getenv("MYSQL_DATABASE"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        host=os.getenv("MYSQL_HOST"),
        port=3306
    )

class TimeLinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb

mydb.connect()
mydb.create_tables([TimeLinePost])

def transform_location(location):
    return location.replace(" ", "+")

# gets corresponding profile data from JSON file
def load_profile_data(profile_name):
    """Load profile data from JSON file"""
    try:
        with open(f'data/{profile_name}.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "name": "Profile Not Found",
            "about": "Profile data not available",
            "work_experiences": [],
            "education": [],
            "hobbies": [],
            "locations": []
        }

@app.route('/')
def index():
    profile = request.args.get('profile', 'ahmad')
    if profile not in ['ahmad', 'rumeza']:
        profile = 'ahmad'
    
    profile_data = load_profile_data(profile)
    
    other_profile = 'rumeza' if profile == 'ahmad' else 'ahmad'
    other_profile_data = load_profile_data(other_profile)

    google_maps_api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    transformed_locations = [transform_location(location) for location in profile_data.get("locations",[])]

    return render_template('index.html', 
                         title=profile_data.get('name', 'MLH Fellow'),
                         profile=profile,
                         other_profile=other_profile,
                         other_profile_name=other_profile_data.get('name', 'Unknown'),
                         profile_img=profile_data.get('img', 'img/profile.png'),
                         about=profile_data.get('about', ''),
                         education=profile_data.get('education', []), 
                         work_experiences=profile_data.get('work_experiences', []), 
                         url=os.getenv("URL"), 
                         locations=",".join(transformed_locations), 
                         google_maps_api_key=google_maps_api_key)

@app.route('/hobbies')
def hobbies_page():
    profile = request.args.get('profile', 'ahmad')
    if profile not in ['ahmad', 'rumeza']:
        profile = 'ahmad'
 
    profile_data = load_profile_data(profile)
    
    other_profile = 'rumeza' if profile == 'ahmad' else 'ahmad'
    other_profile_data = load_profile_data(other_profile)
    
    return render_template('hobbies.html', 
                         title=f"{profile_data.get('name', 'My')} Hobbies", 
                         profile=profile,
                         other_profile=other_profile,
                         other_profile_name=other_profile_data.get('name', 'Unknown'),
                         hobbies=profile_data.get('hobbies', []))

@app.route('/timeline')
def timeline_page():
    return render_template('timeline.html')

@app.route('/api/timeline_post', methods=['POST'])
def post_timeline_post():
    name    = request.form.get('name',   '').strip()
    email   = request.form.get('email',  '').strip()
    content = request.form.get('content','').strip()

    if not name:
        return "Invalid name", 400

    if not content:
        return "Invalid content", 400

    if '@' not in email or '.' not in email:
        return "Invalid email", 400
    
    timeline_post = TimeLinePost.create(name=name, email=email, content=content)

    return model_to_dict(timeline_post)

@app.route('/api/timeline_post', methods=['GET'])
def get_timeline_post():
    return {
        'timeline_posts': [
            model_to_dict(p)
            for p in TimeLinePost.select().order_by(TimeLinePost.created_at.desc())
        ]
    }

@app.route('/api/timeline_post', methods=['DELETE'])
def delete_timeline_post():
    name = request.form['name']
    email = request.form['email']
    content = request.form['content']
    deleted = TimeLinePost.delete().where(
        (TimeLinePost.name == name) &
        (TimeLinePost.email == email) &
        (TimeLinePost.content == content)
    ).execute()
    return {"deleted": deleted}

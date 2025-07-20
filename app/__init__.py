import os
import json
import datetime
from flask import Flask, render_template, request, abort
from dotenv import load_dotenv
from peewee import *
from playhouse.shortcuts import model_to_dict

load_dotenv()
app = Flask(__name__)

mydb = MySQLDatabase(
    os.getenv("MYSQL_DATABASE"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    host=os.getenv("MYSQL_HOST"),
    port=3306,
)
print(mydb)

class TimelinePost(Model):
    name       = CharField()
    email      = CharField()
    content    = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb

mydb.connect()
mydb.create_tables([TimelinePost])

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

@app.route("/timeline")
def timeline_page():
    profile = request.args.get("profile", "ahmad")
    if profile not in ["ahmad", "rumeza"]:
        profile = "ahmad"

    other_profile = "rumeza" if profile == "ahmad" else "ahmad"

    other_profile_data = load_profile_data(other_profile)
    other_profile_name = other_profile_data.get("name", "Unknown")

    # 4) render your new template
    return render_template(
        "timeline.html",
        title=load_profile_data(profile).get("name", "MLH Fellow"),
        profile=profile,
        other_profile=other_profile,
        other_profile_name=other_profile_name
    )

@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    name = request.form['name']
    email = request.form['email']
    content = request.form['content']
    timeline_post = TimelinePost.create(name=name, email=email, content=content)
    print(f"Created Timeline post with id={timeline_post.id}")
    return model_to_dict(timeline_post)

@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return {
        'timeline_posts': [
            model_to_dict(p)
            for p in
TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }

@app.route('/api/timeline_post/<int:post_id>', methods=["DELETE"])
def delete_timeline_post(post_id):
    deleted_count = (TimelinePost.delete().where(TimelinePost.id == post_id).execute())
    if deleted_count:
        return {'status': 'deleted', 'id': post_id}
    return abort(404, description=f"No timeline post with id={post_id}")
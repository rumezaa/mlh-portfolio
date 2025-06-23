import os
import json
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

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

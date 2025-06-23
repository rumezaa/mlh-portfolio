import os
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

def transform_location(location):
    return location.replace(" ", "+")

@app.route('/')
def index():
    # for jinja template, update when that pr is merged
    google_maps_api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    locations = ["Empire State Building, NY"]
    transformed_locations = [transform_location(location) for location in locations]

    return render_template('index.html', title="MLH Fellow", url=os.getenv("URL"), locations=",".join(transformed_locations), google_maps_api_key=google_maps_api_key)



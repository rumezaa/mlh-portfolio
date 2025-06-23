import os
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

def transform_location(location):
    return location.replace(" ", "+")

@app.route('/')
def index():
    work_experiences = [
        {
            'title': 'Production Engineer',
            'company': 'Meta & Major League Hacking',
            'date': 'Jun 2025 - Present',
            'details': [
                "Developing skills in DevOps, infrastructure, and distributed systems as a Production Engineering Fellow, focusing on the principles of reliability and scalability that power Meta's services."
            ]
        },
        {
            'title': 'Software Engineer Intern, HBO Max',
            'company': 'Warner Bros. Discovery',
            'date': 'Jun 2025 - Present',
            'details': [
                "Contributing to the GCX Instrumentation Tooling team for HBO Max, utilizing Kotlin and TypeScript to enhance monitoring and content delivery systems."
            ]
        },
        {
            'title': 'Software Engineer Intern',
            'company': 'New England Investment Consulting Group',
            'date': 'May 2024 – Aug 2024',
            'details': [
                "Engineered a full-stack AI-driven school platform for over 1,000 students using React, TypeScript, and Python.",
                "Implemented a Go microservice and set up a full CI/CD pipeline with AWS, Jenkins, and Docker, cutting deployment times by 30%."
            ]
        }
    ]
    education = [
        {
            'degree': 'B.S. in Computer Engineering',
            'school': 'CUNY College of Staten Island',
            'date': 'Expected May 2026',
            'details': [
                '<strong>Minor:</strong> Computer Science | <strong>GPA:</strong> 3.9 / 4.0',
                '<strong>Relevant Coursework:</strong> Object Oriented Programming, Operating Systems, Data Structures, System Design.',
                '<strong>Affiliations:</strong> CodePath TA, CUNY Tech Prep, SEO, CS Club.'
            ]
        }
    ]

    google_maps_api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    locations = ["Empire State Building, NY"]
    transformed_locations = [transform_location(location) for location in locations]

    return render_template('index.html', title="MLH Fellow", education=education, work_experiences=work_experiences, url=os.getenv("URL"), locations=",".join(transformed_locations), google_maps_api_key=google_maps_api_key)

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

# MLH Portfolio - Dual Profile Portfolio Site

Welcome to our MLH Fellowship Portfolio! This is a Flask-based portfolio site featuring dual profiles for Ahmad Basyouni and Rumeza Fatima, with dynamic content loading from JSON files and a toggle functionality to switch between profiles.

## Features

### 🎯 Dual Profile System
- **Dynamic Profile Switching**: Toggle between Ahmad and Rumeza's profiles using the header button
- **JSON-Based Content**: All profile data is loaded from `data/ahmad.json` and `data/rumeza.json`
- **Consistent Navigation**: Maintains profile context across Home and Hobbies pages
- **URL Query Parameters**: Uses `?profile=ahmad` or `?profile=rumeza` for clean URLs

### 🎨 Dynamic Theming
- **Ahmad's Theme**: Blue color scheme (#1C539F) with yellow toggle button
- **Rumeza's Theme**: Purple color scheme (#8A6AC9) with yellow toggle button and purple text


### 📱 Portfolio Sections
- **About Me**: Personal descriptions and background
- **Work Experience**: Detailed work history with company, dates, and achievements
- **Education**: Academic background and relevant coursework
- **Hobbies**: Personal interests with images and descriptions
- **Interactive Map**: Google Maps integration showing travel locations

## Technical Implementation

### Flask Backend
- **Dynamic Routes**: Single routes with query parameter handling
- **JSON Data Loading**: Modular data loading from JSON files
- **Template Inheritance**: Consistent layout across pages
- **Error Handling**: Graceful fallbacks for missing data

### Frontend Features
- **Conditional Styling**: CSS classes that change based on active profile
- **Responsive Navigation**: Clean header with profile toggle button
- **Modern CSS**: Flexbox layouts, smooth transitions, and hover effects

## Getting Started

### Prerequisites
- Python 3.x
- pip package manager

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd mlh-portfolio
```

2. **Create and activate virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: python3-virtualenv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env
# Edit .env file with your Google Maps API key and other variables
# Required: GOOGLE_MAPS_API_KEY - Get from Google Cloud Console

```

5. **Run the application**
```bash
export FLASK_ENV=development
flask run
```

The application will be available at `http://127.0.0.1:5000/`

## Usage

### Profile Navigation
- **Default View**: Visit `/` to see Ahmad's profile
- **Rumeza's Profile**: Visit `/?profile=rumeza` or click the toggle button
- **Hobbies Page**: Visit `/hobbies` or `/hobbies?profile=rumeza`
- **Toggle Button**: Click "Switch to [Name]" in the header to change profiles

### Data Management
- **Ahmad's Data**: Edit `data/ahmad.json` to update Ahmad's information
- **Rumeza's Data**: Edit `data/rumeza.json` to update Rumeza's information
- **Profile Images**: Place images in `app/static/img/` and reference in JSON files

## Project Structure

```
mlh-portfolio/
├── app/
│   ├── __init__.py          # Flask app configuration and routes
│   ├── static/
│   │   ├── styles/
│   │   │   └── main.css     # Styling with conditional themes
│   │   └── img/             # Profile images and assets
│   │       └── hobby/       # Hobby images
│   └── templates/
│       ├── index.html       # Main portfolio page
│       └── hobbies.html     # Hobbies page
├── data/
│   ├── ahmad.json          # Ahmad's profile data
│   └── rumeza.json         # Rumeza's profile data
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Customization

### Adding New Profiles
1. Create a new JSON file in `data/` (e.g., `data/newprofile.json`)
2. Follow the existing JSON structure with name, about, work_experiences, education, hobbies, and img fields
3. Update the Flask routes to include the new profile option

### Styling Changes
- **Color Themes**: Modify the CSS variables in `app/static/styles/main.css`
- **Layout**: Update the HTML templates in `app/templates/`
- **Images**: Replace images in `app/static/img/` and update JSON references

## License

This project is part of the MLH Fellowship program.

---

**Built with 💜 using Flask, HTML, CSS, and JavaScript**

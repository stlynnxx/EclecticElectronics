import os
import uuid
import json
from flask import Flask, render_template,request, redirect, url_for, current_app
from werkzeug.utils import secure_filename

import random


app = Flask(__name__)

ALLOWED_EXTENSIONS = {"png", "webp", "jpg", "jpeg", "gif"}
def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
DATA_FILE = "Quotes.json"
DATA_DIR = os.environ.get("DATA_DIR", "./data")
os.makedirs(DATA_DIR, exist_ok=True)
QUOTES_FILE = os.path.join(DATA_DIR, DATA_FILE)
UPLOAD_FOLDER = os.path.join(DATA_DIR, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.route('/')
def home():

    return render_template('home.html')
@app.route('/eclecticAI')
def eclecticAI():
    return render_template('eclecticAI.html')
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/quote')
def quote():
    return render_template('quote.html')
@app.route('/gallery')
def gallery():
    return render_template('gallery.html')
@app.route('/contact')
def contact():
    return render_template('contact.html')
@app.route('/password')
def password():


    return render_template('passwordgenerator.html')

@app.route('/generator')
def generator():
    adjs = ["Attractive", "Agreeable", "Angry", "Big",
            "Bald", "Ambitious", "Bewildered", "Colossal",
            "Beautiful", "Brave", "Clumsy", "Fat", "Chubby",
            "Calm", "Defeated", "Gigantic", "Clean", "Delightful", "Cold",
            "Patient", "Serene", "Empty", "Soft", "Pink", "Purple", "Golden",
            "Blue", "Aquamarine", "Lavender", "Green", "Teal", "Red", "Crimson",
            "Purple", "Orange", "Sandy", "Silver", "Grey", "Cursed", "Forgotten",
            "Forsaken", "Bitter", "Forlorn", "Wet","Warm", "Glassy", "Clicky", "Clacky",
            "Salty", "Tidal", "Oceanic", "Sweet", "Fabulous", "Dancing", "Fantastic",
            "Advanced", "Chronic", "Dank", "Slippery", "Icy", "Energetic", "Glassy",
            "Pure", "Impure", "Superb", "Agentic", "Nightmarish", "Dreamlike",
            "Ethereal", ""]
    nouns = ["Airplane", "Bell", "Belt", "Newspaper", "Owl", "Lizard",
             "Lunch", "Sun", "Slinky", "Sheep", "Kangaroo", "Hair", "Helicopter", "Cup",
             "Straw", "Torch", "Wood", "Tower", "Zygon", "Borg", "Tardis", "Dog", "Cat",
             "Beagle", "Pudding", "Wall", "Desk", "Window", "Box", "Book", "Scarf","Jar",
             "Screen", "Wrist", "Keyboard", "Drawer", "Fez", "Singer", "Machine",
             "Puck", "Brush", "Lamp", "Heart", "Coaster", "Router", "Shelf",
             "Gamer", "Coffee", "Snake", "Tank", "Stove", "Oven", "Car", "Truck",
             "Fireplace", "Phone", "Mirror", "Paint", "Tablet", "Pad", "Gnome",
             "Elf"]
    specials = ["!","?","@","#","$", "%","^", "&","*","+"]

    adj_pick = random.choice(adjs)
    noun_pick = random.choice(nouns)
    special_pick = random.choice(specials)
    random_one = random.randint(0, 9)
    random_two = random.randint(0, 9)
    proto_password = adj_pick + noun_pick
    num_1 = str(random_one)
    num_2 = str(random_two)
    password = proto_password + num_1 + num_2 + special_pick
    return render_template('passwordgenerator.html', password=password)

@app.route('/quotesubmit', methods=['POST'])

def quotesubmit():

    passer = []
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    email = request.form.get('email')
    telephone = request.form.get('tel')
    preferred = request.form.get('preferred')
    details = request.form.get('details')
    photo = request.files.get('photo')
    photo_url = None
    if photo and photo.filename:
        if not allowed_file(photo.filename):
            return "Unsupported file type", 400
    # Sanitize
        original = secure_filename(photo.filename)
        ext = original.rsplit('.', 1)[1].lower()
        new_name = f"{uuid.uuid4().hex}.{ext}"
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], new_name)
        photo.save(save_path)
        photo_url = f"/uploads/{new_name}"
    entry = {
        'fname': fname,
        'lname': lname,
        'email': email,
        'telephone': telephone,
        'preferred': preferred,
        'details': details,
        'photo_url': photo_url,
    }
    if os.path.exists(QUOTES_FILE):
        with open(QUOTES_FILE, 'r', encoding="utf-8") as f:
            passer = json.load(f)
    else:
        passer = []

    passer.append(entry)
    with open(QUOTES_FILE, 'w', encoding='utf-8') as f:
        json.dump(passer, f, indent=2)

    return redirect(url_for('quote'))





if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

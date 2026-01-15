import os

from flask import Flask, render_template, jsonify
import random


app = Flask(__name__)




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
            "Salty", "Tidal", "Oceanic", "Sweet"]
    nouns = ["Airplane", "Bell", "Belt", "Newspaper", "Owl", "Lizard",
             "Lunch", "Sun", "Slinky", "Sheep", "Kangaroo", "Hair", "Helicopter", "Cup",
             "Straw", "Torch", "Wood", "Tower", "Zygon", "Borg", "Tardis", "Dog", "Cat",
             "Beagle", "Pudding", "Wall", "Desk", "Window", "Box", "Book", "Scarf","Jar",
             "Screen", "Wrist", "Keyboard"]
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







if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

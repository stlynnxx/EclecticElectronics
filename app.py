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
@app.route('/run-python', methods=['POST'])
def run_python():
    adjs = ["Attractive", "Agreeable", "Angry", "Big",
            "Bald", "Ambitious", "Bewildered", "Colossal",
            "Beautiful", "Brave", "Clumsy", "Fat", "Chubby",
            "Calm", "Defeated", "Gigantic", "Clean", "Delightful"]
    nouns = ["Airplane", "Bell", "Belt", "Newspaper", "Owl","Lizard",
             "Lunch", "Sun", "Slinky", "Sheep", "Kangaroo", "Hair", "Helicopter"  ]


    adj_pick = random.choice(adjs)
    noun_pick = random.choice(nouns)
    random_one = random.randint(0,9)
    random_two = random.randint(0,9)
    password = adj_pick + noun_pick + random_one + random_two
    print(password)
    return jsonify({'password': password})








if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0')

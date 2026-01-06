from flask import Flask, render_template
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
    adjs = ["Attractive", "Agreeable", "Angry", "Big",
            "Bald", "Ambitious", "Bewildered", "Colossal",
            "Beautiful", "Brave", "Clumsy", "Fat", "Chubby",
            "Calm", "Defeated", "Gigantic", "Clean", "Delightful"]
    nouns = ["Airplane", "Bell", "Belt", "Newspaper", "Owl","Lizard",
             "Lunch", "Sun", "Slinky", "Sheep", "Kangaroo", "Hair", "Helicopter"  ]
    randoms = []
    alphabet = ["A","a","B","b","C","c","D","d","E","e"
                "F","f","G","g","H","h","I","i","J","j"
                "K","k","L","l","M","m","N","n","O","o"
                "P","p","Q","q","R","r","S","s"
                "T","t","U","u","V","v","W","w"
                "X","x","Y","y","Z","z"]
    value_one = random.randint(1,9)
    value_two = random.randint(1,9)
    value_three = random.randint(1,9)
    for i in value_three:
       randoms = [random.choice(alphabet)]
    





if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=6969)

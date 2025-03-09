import pickle
from flask import Flask, request, render_template, flash, redirect, url_for
from math import ceil

app = Flask(__name__)
app.secret_key = '234567ygfdsweghy654321wedfe'
model = pickle.load(open("university.pkl", "rb"))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def admin():
    gre = request.form["gre"]
    tofl = request.form["tofl"]
    rating = request.form["rating"]
    sop = request.form["sop"]
    lor = request.form["lor"]
    cgpa = request.form["cgpa"]
    research = request.form["research"]

    if not gre or not tofl or not rating or not sop or not lor or not cgpa:
        flash("Please fill in all fields.")
        return redirect(url_for('index'))

    try:
        gre = float(gre)
        tofl = float(tofl)
        rating = float(rating)
        sop = float(sop)
        lor = float(lor)
        cgpa = float(cgpa)

        gre = (gre - 290) / (340 - 290)
        tofl = (tofl - 92) / (120 - 92)
        rating = (rating - 1.0) / 4.0
        sop = (sop - 1.0) / 4.0
        lor = (lor - 1.0) / 4.0
        cgpa = (cgpa - 290.0) / (340.0 - 290.0)

        if research == "Yes":
            research = 1
        else:
            research = 0

        preds = [[gre, tofl, rating, sop, lor, cgpa, research]]
        xx = model.predict(preds)

        if xx > 0.5:
            return render_template("chance.html", p=str(ceil(xx[0]*100))+"%")
        return render_template("nochance.html")
    except ValueError:
        flash("Invalid input. Please enter numerical values for GRE, TOEFL, Rating, SOP, LOR, and CGPA.")
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=False)
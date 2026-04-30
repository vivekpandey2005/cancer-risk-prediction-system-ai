from flask import Flask, render_template, request, jsonify, redirect, session
from openai import OpenAI
from flask_cors import CORS
import PyPDF2

import os
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)
app.secret_key = "123"
users = {}
CORS(app)


class DummyModel:
    def predict(self, age, smoking, family):
        reasons = []
        risk_score = 0

        # Scoring logic
        if age > 60:
            risk_score += 2
            reasons.append("Age > 60 is a significant risk factor.")
        elif age > 40:
            risk_score += 1
            reasons.append("Age > 40 is a moderate risk factor.")

        if smoking == 1:
            risk_score += 2
            reasons.append("Smoking significantly increases health risk.")
        if family == 1:
            risk_score += 2
            reasons.append("Family history indicates a genetic predisposition.")

        result = 1 if risk_score >= 3 else 0

        if not reasons:
            explanation = "No major risk factors detected based on provided data."
        else:
            explanation = "Factors found: " + " ".join(reasons)

        return result, explanation


model = DummyModel()


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/precautions')
def precautions():
    return render_template('precautions.html')


@app.route('/cure')
def cure():
    return render_template('cure.html')


@app.route('/feedback')
def feedback():
    return render_template('feedback.html')


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/statistics')
def statistics():
    return render_template('statistics.html')

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    msg = data.get("message", "").lower()

    # greetings
    if any(word in msg for word in ["hello", "hi", "hey"]):
        reply = "Hello 👋 How can I help you?"

    # name
    elif "name" in msg:
        reply = "I am your free chatbot 🤖"

    # how are you
    elif "how are you" in msg:
        reply = "I'm doing great 😊 Thanks for asking!"

    # cancer / health basic info
    elif "cancer" in msg:
        reply = (
            "Cancer is a disease where cells in the body grow abnormally and spread. "
            "It can affect different parts of the body. Early detection and treatment are very important."
        )

    # education / general info
    elif "what is" in msg:
        reply = "I can try to help 😊 Please ask a simpler question or I will improve over time."

    elif "bye" in msg:
        reply = "Goodbye 👋 Have a nice day!"

    else:
        reply = "Sorry 😊 I am still learning. Try asking something simple."

    return jsonify({"reply": reply})

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        age = int(data['age'])
        smoking = int(data['smoking'])
        family = int(data['family'])

        result, explanation = model.predict(age, smoking, family)
        output = "High Risk ⚠️" if result == 1 else "Low Risk ✅"

        return jsonify({"result": output, "explanation": explanation})

    except Exception as e:
        return jsonify({"result": "Error", "error": str(e)})

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        users[username] = password
        return redirect("/login")

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users and users[username] == password:
            session["user"] = username
            return redirect("/")
        else:
            return "Wrong username or password"

    return render_template("login.html")







@app.route('/home')
def home():
    return render_template('home.html')



@app.route('/main')
def main():
    return render_template('index.html')




@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)
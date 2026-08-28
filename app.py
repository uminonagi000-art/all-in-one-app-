from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def home():
  return render_template("index.html")


@app.route("/dashboard", methods=["POST"])
def dashboard():
  language = request.form.get("language")
  category = request.form.get("category")
  return f"Successfully processed! Language: {language}, Category: {category}"


if __name__ == "__main__":
  app.run(debug=True)
    

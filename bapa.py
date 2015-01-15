from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "Hello Bay Area Paragliders!"

if __name__ == "__main__":
    app.run()


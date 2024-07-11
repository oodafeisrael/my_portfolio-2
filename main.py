from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route('/test')
def test():
    return 'This is for testing purpose'

@app.route('/home')
def home():
    return 'This is my Home page'


if __name__=="__main__":
    # start the flask development server
    # Listen on all available interfaces (0.0.0.0) and port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)


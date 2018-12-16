from flask import Flask, render_template, request
# initializing a variable of Flask
app = Flask(__name__)


# decorating index function with the app.route
@app.route('/login', methods=['GET'])
def index():
    colours = ['Red', 'Blue', 'Black', 'Orange']
    return render_template('login.html')


if __name__ == "__main__":
    app.run()

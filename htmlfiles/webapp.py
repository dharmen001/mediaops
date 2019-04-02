# coding=utf-8
# !/usr/bin/env python


from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

# @ signifies a decorator - way to wrap a function and modifying its behaviour


@app.route("/")
@app.route("/home")
def home():
    return render_template('FlaskApp.html')


@app.route('/Submit', methods=['POST'])
def submit():
    report = request.form['reports']

    if report == 'Generate Jira Tickets':
        subprocess.call([r'C:\mediaops\script\GenerateJiraTickets.bat'])
        return 'Generate Jira Tickets submitted'
    elif report == 'NDP Reports':
        subprocess.call([r'C:\mediaops\script\Ndp.bat'])
        return 'NDP Reports Generated'
    elif report == 'Billing':
        subprocess.call([r'C:\mediaops\script\Billing.Bat'])
        return render_template('Billing.html')


if __name__ == "__main__":
    app.run(debug=True, host='localhost',  port=8080)

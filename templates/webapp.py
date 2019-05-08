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
        subprocess.call([r'/home/groupm/mediaops-project/mediaops/script/jira.sh'])
        return 'Generate Jira Tickets submitted'
    elif report == 'NDP Reports':
        subprocess.call([r'/home/groupm/mediaops-project/mediaops/script/NdpMonthEndProcess.sh'])
        return 'NDP Reports Generated'
    elif report == 'Billing EMails':
        subprocess.call([r'/home/groupm/mediaops-project/mediaops/script/BillingEmails.sh'])
        return 'Billing Emails sent'
    elif report == 'Adwords Reports':
        subprocess.call([r'/home/groupm/mediaops-project/mediaops/script/Adwords.sh'])
        return 'Adwords Files Generated'
    elif report == 'DCM Impressions Tag Rajiv':
        subprocess.call([r'/home/groupm/mediaops-project/mediaops/script/RajivImpressionEventTag.sh'])
        return 'Impressions Tag Generated'
    elif report == 'DCM Impressions Tag Puneet':
        subprocess.call([r'/home/groupm/mediaops-project/mediaops/script/PuneetImpressionEventTag.sh'])
        return 'Impressions Tag Generated'


if __name__ == "__main__":
    # Debug/Development
    # app.run(debug=True, host="0.0.0.0", port="5000")
    # Production
    app.run(debug=False, host='0.0.0.0',  port=5000)
    # http_server = WSGIServer(('0.0.0.0', 5000), app)
    # http_server.serve_forever()


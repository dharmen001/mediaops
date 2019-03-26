# coding=utf-8
# !/usr/bin/env python

from Classes.DataReaders import OutlookNdpDownload
from flask import Flask, render_template
from Classes.NdpTickets.Advertiser_list import AdvertiserList
from Classes.NdpTickets.JiraWrapper import Jira
from Classes.DataReaders.config_ini import Config
import subprocess
app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/Submit', methods=['POST'])
def submit():
    subprocess.call([r'C:\mediaops\script\Ndp.bat'])
    # object_outlook = OutlookNdpDownload.Outlook()
    # object_outlook.main()
    return 'Report Generated'


if __name__ == "__main__":
    app.run(debug=True, host='localhost',  port=8080)

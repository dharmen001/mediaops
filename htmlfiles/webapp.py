from Classes.DataReaders import OutlookNdpDownload
from flask import Flask, render_template
app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/Submit')
def submit():
    object_outlook = OutlookNdpDownload.Outlook()
    object_outlook.main()
    return 'Report Generated'


if __name__ == "__main__":
    app.run(debug=True)
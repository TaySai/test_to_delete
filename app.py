import fetch_data.web as wb
import fetch_data.batch as btch
from flask import Flask, request, render_template
from flask import jsonify

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template("home.html")


# Return information about one galaxy
@app.route("/api/v1/web", methods=['GET', 'POST'])
def api_v1_web():
    galaxy = request.args.get('galaxy', default=None)
    messier = request.args.get('messier', default=None)
    if messier is not None or galaxy is not None:
        res = wb.get_data(galaxy, messier)
        return jsonify(res)
    else:
        return "Expected at least one good parameter \n <br>" \
               "example /api/v1/web?messier=example1 \n <br>" \
               "example /api/v1/web?galaxy=example2 \n <br>" \
               "example /api/v1/web?messier=example1&galaxy=example2"


# Return information about one galaxy
@app.route("/api/v1/batch/", methods=['GET'])
def api_v1_batch():
    try:
        if request.headers['Content-Type'] == 'application/json':
            data = request.get_json()
            res = btch.get_data(data)
            if data is None:
                return 'Error, expected data'
            return jsonify(res)
    except:
        return "Expected header 'Content-Type': 'application/json'"


# Return web page
@app.route("/galaxies", methods=['GET'])
def web_galaxies():
    res = wb.get_galaxies()
    return render_template("distinct_data.html", res=res, title='galaxies')

# Return web page
@app.route("/messiers", methods=['GET'])
def web_messiers():
    res = wb.get_messiers()
    return render_template("distinct_data.html", res=res, title='messiers')

# Return web page
@app.route("/galaxies/<galaxy>", methods=['GET'])
def web_galaxy(galaxy):
    return "Development in progress..."

# Return web page
@app.route("/messiers/<messier>", methods=['GET'])
def web_messier(messier):
    res = wb.get_endpoint_web_messier(messier)
    return render_template("messier.html", res=res)

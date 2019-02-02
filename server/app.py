from flask import jsonify, Flask, request, abort, make_response
#from flask_cors import CORS
from xmltojson import getInfo, getCatchword

app = Flask(__name__)
#CORS(app)


@app.route('/search', methods=['GET','POST'])
def search():
    if not request.json or not 'name' in request.json:
        abort(400)
    #print request
    jdata = getInfo(request.json['name'])
    return jsonify(jdata)
    
@app.route('/searchBy', methods=['GET','POST'])
def searchBy():
    #print request
    search = request.args.get("name")
    #print search
    jdata = getInfo(search)
    return jsonify(jdata)


@app.route('/getCatchword', methods=['GET', 'POST'])
def getCat():
    if not request.json or not 'name' in request.json:
        abort(400)
    # \'No catchword\' will be skipped
    
    jdata = getCatchword(request.json['name'])
    return jsonify(jdata)
    
@app.route('/getCatchwordBy', methods=['GET', 'POST'])
def getCatBy():
    name = request.args.get("name")
    # \'No catchword\' will be skipped
    
    jdata = getCatchword(name)
    return jsonify(jdata)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/')
def hello():
    return "LIT2019"

if __name__ == "__main__":
    app.run(host= '0.0.0.0')

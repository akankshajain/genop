# Using flask to make an api
# import necessary libraries and functions
import genoperator
from utils import operators_dict
from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from flask_cors import CORS, cross_origin

# creating a Flask app
app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app, resources={r"/download": {"origins": "http://localhost:5000"}})
# on the terminal type: curl http://127.0.0.1:5000/
# returns hello world when we use GET.
# returns the data that we send when we use POST.
#@app.route('/', methods = ['GET', 'POST'])
#def create_oper():
#    if(request.method == 'GET'):

        #data = "hello world"
    #data = request.get_json()
    #return jsonify({'data': data})

####################API Routes########################

# List already created operators
@app.route('/list_opers', methods = ['GET'])
@cross_origin(origin='localhost',headers=['Content-Type','application/json'])
def list_opers():
    if(request.method == 'GET'):
        return operators_dict()


#Create helm operator out of helm chart
@app.route('/helmoperator', methods = ['POST'])
def createhelmoperator():
    content = request.json
    genoperator.helmoperator(content['helmrepo'],content['helmchartname'],content['operatorname'])  
    # return jsonify({'data': chart_name})
    return "Operator created!"

#Create ansible operator out of the k8s resources in a namespace
@app.route('/ansibleoperator', methods = ['POST'])
def createansibleoperatorfromk8s():
    content = request.json
    
    genoperator.ansibleoperatorfromk8s(content['groupname'],content['domainname'],content['operatorname'],content['version'],content['kinds'],content['namespace'])  
    # return jsonify({'data': chart_name})
    return "Operator created!"
    
#Create ansible operator from scratch
@app.route('/ansibleoperatorscratch', methods = ['POST'])
def createansibleoperatorfromscratch():
    content = request.json

    genoperator.ansibleoperatorfromscratch(content['groupname'],content['domainname'],content['operatorname'],content['version'],content['kinds'])
    # return jsonify({'data': chart_name})
    return "Operator created!"

####################Front end Routes########################

@app.route('/')
def dashboard():
    return render_template('index.html')

@app.route('/operators/create')
def create_operator():
    return render_template('createOperator.html')

@app.route('/operators')
def list_operators():
    return render_template('operators.html')

@app.route('/secrets')
def list_secrets():
    return render_template('secrets.html')

@app.route('/operators/scratch')
def create_operator_scratch():
    return render_template('createOperatorScratch.html')

# Main invocation
if __name__ == '__main__':

    #app.run(debug = True)
    app.run(debug = True, host='9.30.199.16', port=5000)


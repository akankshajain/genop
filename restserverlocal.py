# Using flask to make an api
# import necessary libraries and functions
import os
import paramiko
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

# creating a Flask app
app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app, resources={r"/download": {"origins": "http://localhost:5000"}})


@app.route('/download', methods=['POST'])
@cross_origin(origin='localhost', headers=['Content-Type', 'application/json'])
def download_operator():
    # curl -i -H "Content-Type: application/json" -X POST -d '{"operator":"nodered-operator-demo","path":"/c/dashdbrepos"}' http://localhost:5000/download
    data = request.get_json()
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('9.30.199.16', username='root', password='akkaFyre2021!Fyre')
    client.exec_command('rm -rf /tmp/' + data['operator'])
    client.exec_command('tar -cvf /tmp/' + data['operator'] + '.tar /root/operators/' + data['operator'])
    print('tar -cvf /tmp/' + data['operator'] + '.tar /root/operators/' + data['operator'])
    os.system("command")
    client.close()
    print('scp root@9.30.199.16:/tmp/' + data['operator'] + '.tar' + " " + data['path'])
    os.system('scp root@9.30.199.16:/tmp/' + data['operator'] + '.tar' + " " + data['path'])
    return jsonify({'data': "hello"})


# Main invocation
if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)

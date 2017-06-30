from flask import Flask, request, render_template
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask.ext.jsonpify import jsonify
from gmusicapi import Mobileclient
import pymongo, socket
from pymongo import MongoClient

app = Flask(__name__)

mobile_client_handle = Mobileclient()
logged_in = mobile_client_handle.login('sy.yousuf9106@gmail.com', '9881880422', Mobileclient.FROM_MAC_ADDRESS)
# socket_handle = socket.socket()

db_handle = MongoClient('mongodb://localhost:27017/')
db = db_handle['project_heights']
accounts_collection = db['accounts']

@app.route('/search/<asset_name>')
def search(asset_name):
	search_result = mobile_client_handle.search(asset_name, max_results=50)   
   	song_hits = search_result['song_hits']
   	search_result_array = []
   	for item in song_hits:
   		search_result_array.append({'title':item['track']['title'], 'storeId':item['track']['storeId'], 'album':item['track']['album'], 'artist':item['track']['artist']})
   	return jsonify(search_result_array)
	
@app.route('/stream/<song_id>')
def get_streaming_url(song_id):
	stream_url_result = mobile_client_handle.get_stream_url(song_id)		        
	return stream_url_result

@app.route('/login', methods=['POST'])
def login():
  username = request.form['username']
  password = request.form['password']
  accounts_db = db.accounts
  result = accounts_db.find_one({'username': username,'password': password})
  if result == None:
    return jsonify({'status':'failed', 'message':'username, password combination not found'})
  else:
    # host_name = socket.gethostname()
    # port = 3000
    # socket_handle.bind((host_name, port))
    # socket_handle.listen()
    return render_template('dashboard.html', value=result['hash'])

if __name__ == '__main__':
     app.run(port='5002')
     
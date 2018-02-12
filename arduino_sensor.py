#!flask/bin/python
from flask import Flask, jsonify, make_response, request
from app import app
from app.models import GPS, Device

app = Flask(__name__)
@app.route('/')
def index():
	return "Hello, World!"

@app.route('/gps', methods=['POST'])
def create_task():
	if not request.json or not 'title' in request.json:
		abort(400)
	gps_data = GPS()
	
	gps_data.id = 0 #need to figure out how to increase the number
	gps_data.utc = request.json['utc']
	gps_data.latitude = request.json['latitude']
	gps_data.longitude = request.json['longitude']
	gps_data.hdop = request.json['hdop']
	gps_data.altitude = request.json['altitude']
	gps_data.fix = request.json['fix']
	gps_data.cog = request.json['cog']
	gps_data.spkm = request.json['spkm']
	gps_data.date = request.json['date']
	gps_data.nsat = request.json['nsat']
	
	#add to the database here
	return jsonify({'task': task}), 201

@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
	app.run(debug=True)


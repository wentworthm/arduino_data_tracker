#!flask/bin/python
#import six
from flask import Flask, jsonify, abort, request, make_response, url_for
from app.models import Device, GPS, DeviceSchema, GPSSchema
import os
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import datetime

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'crus.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

gps_schema = GPSSchema()
gpss_schema = GPSSchema(many=True)
device_schema = DeviceSchema()
devices_schema = DeviceSchema(many=True)

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Device': Device, 'GPS': GPS}

@app.errorhandler(400)
def bad_request(error):
	return make_response(jsonify({'error': 'Bad request'}), 400)
	
@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)
		
@app.route('/p1/device', methods=['GET'])
def get_devices():
	all_devices = Device.query.all()
	result = devices_schema.dump(all_devices)
	return jsonify(result.data)
	
@app.route('/p1/device/<int:device_id>', methods=['GET'])
def get_device(device_id):
	if device_id == 0:
		abort(404)
	device = Device.query.get(device_id)
	return device_schema.jsonify(device)
	
@app.route('/p1/device', methods=['POST'])
def add_device():
	if not request.json or 'name' not in request.json:
		abort(400)
		
	name = request.json['name']
	simid = request.json['simid']
	registerutc = register.json['registerutc']
	
	new_device = Device(name, simid, registerutc)
	
	db.session.add(new_device)
	db.session.commit()
	
	return jsonify(new_device)

@app.route('/p1/device/<int:device_id>',  methods=['PUT'])
def update_device(device_id):
	if device == 0:
		abort(404)
	if not request.json:
		abort(400)
	if 'name' in request.json: # and not isinstance(request.json['name'], six.string_types):
		abort(400)
	if 'simid' in request.json: # and not isinstance(request.json['simid'], six.string_types):
		abort(400)
	if 'registerutc' in reuqest.json and not isinstance(request.json['registerutc'], DateTime):
		abort(400)
	device = Device.query.get(device_id)
	name = request.json['name']
	simid = request.json['simid']
	registerutc = request.json['registerutc']
	
	device.name = name
	device.simid = simid
	device.registerutc = registerutc
	
	db.session.commit()
	return device_schema.jsonify(user)
	
@app.route('/p1/device/gps<int:device_id>', methods=['GET'])
def get_gps_device():
	all_gps = GPS.query.all()
	result = gps_schema.dump(all_gps)
	return jsonify(result.data)
	
@app.route('/p1/gps/<int:gps_id>', methods=['GET'])
def get_gps(gps_id):
	if gps_id == 0:
		abort(404)
	gps = GPS.query.get(gps_id)
	return gps_schema.jsonify(gps)
	
@app.route('/p1/gps', methods=['POST'])
def add_gps():
	if not request.json or 'name' not in request.json:
		abort(400)
	
	device_id = request.json['device_id']
	utc = request.json['utc']
	latitude = request.json['latitude']
	latDir = request.json['latDir']
	longitude = request.json['longitude']
	longDir = request.json['longDir']
	hdop = request.json['hdop']
	altitude = request.json['altitude']
	fix = request.json['fix']
	cog = request.json['cog']
	spkm = request.json['spkm']
	spkn = request.json['spkn']
	date = request.json['date']
	nsat = request.json['nsat']
	
	new_gps = GPS(device_id, utc, latitude, latDir, \
		longitude, longDir, hdop, altitude, fix, cog, \
		spkm, spkn, date, nsat)
	
	db.session.add(new_device)
	db.session.commit()
	
	return jsonify(new_device)

if __name__ == '__main__':
    app.run(debug=True)

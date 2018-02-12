from app import db
import datetime
from flask_marshmallow import Marshmallow

class GPS(db.Model):
#	__table_args__ = {'extend_existing': True} 
	id = db.Column(db.Integer, primary_key=True)
	device_id = db.Column(db.Integer, db.ForeignKey('device.id'))
	utc = db.Column(db.Time)
	latitude = db.Column(db.Float)
	latDir = db.Column(db.String(1))
	longitude = db.Column(db.Float)
	longDir = db.Column(db.String(1))
	hdop = db.Column(db.Float)
	altitude = db.Column(db.Float)
	fix = db.Column(db.SmallInteger)
	cog = db.Column(db.Float)
	spkm = db.Column(db.Float)
	spkn = db.Column(db.Float)
	date = db.Column(db.Date)
	nsat = db.Column(db.SmallInteger)
	
	def __init__(self, device_id, utc, latitude, latDir, \
				 longitude, longDir, hdop, altitude, fix, cog, \
				 spkm, spkn, date, nsat):
		self.device_id = device_id
		self.utc = utc
		self.latitude = latitude 
		self.latDir = latDir
		self.longitude = longitude
		self.longDir = longDir
		self.hdop = hdop
		self.altitude = altitude
		self.fix = fix
		self.cog = cog
		self.spkm = spkm
		self.spkn = spkn
		self.date = date
		self.nsat = nsat
	
	def __repr__(self):
		return '<Date {}>'.format(self.date) \
			+ '\n<Time {}>'.format(self.time) \
			+ '\n<Latitude {}>'.format(self.latitude + self.latDir) \
			+ '\n<Longitude {}>'.format(self.longitude + self.longDir)

class GPSSchema(Marshmallow().Schema):
	class Meta:
		fields = ('device_id', 'utc', 'latitude', 'latDir', \
				 'longitude', 'longDir', 'hdop', 'altitude', 'fix', 'cog', \
				 'spkm', 'spkn', 'date', 'nsat')

class Device(db.Model):
#	__table_args__ = {'extend_existing': True} 
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), index=True, unique=True)
	simid = db.Column(db.String(22), index=True, unique=True)
	registerutc = db.Column(db.DateTime, index=True, default=datetime.datetime.utcnow)
	gpss = db.relationship('GPS', backref='author', lazy='dynamic')
	
	def __init__(self, name, simid, registerutc):
		self.name = name
		self.simid = simid
		self.registerutc = registerutc
	
	def __repr__(self):
		return '<Device Name {}>'.format(self.name) \
			+ '\n<Sim ID {}>'.format(self.simid)

class DeviceSchema(Marshmallow().Schema):
	class Meta:
			fields = ('name', 'simid', 'registerutc')

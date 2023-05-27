from database import db

class VesselData(db.Model):
    __tablename__ = 'vessel_data'
    
    id = db.Column(db.Integer, primary_key=True)
    mmsi = db.Column(db.BigInteger)
    shipname = db.Column(db.String(100))
    navigationalstatus = db.Column(db.Integer)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    timestamp = db.Column(db.DateTime)

    def to_dict(self):
        return {
            'id': self.id,
            'mmsi': self.mmsi,
            'name': self.shipname,
            'navigationalstatus': self.navigationalstatus,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'timestamp': self.timestamp.isoformat()
        }

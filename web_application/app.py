import os
import json
from flask import Flask, render_template, jsonify
from models import VesselData
from database import db
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime, timedelta

def delete_old_data():
    # Print out a message when the function is invoked.
    print(f"{datetime.now()}: Running delete_old_data")
    
    one_month_ago = datetime.now() - timedelta(days=30)
    old_data = VesselData.query.filter(VesselData.timestamp < one_month_ago).delete()
    db.session.commit()

STATUS_DICT = {
    "0" : "Under way using engine",
    "1" : "At anchor",
    "2" : "Not under command",
    "3" : "Restricted manoeuverability",
    "4" : "Constrained by her draught",
    "5" : "Moored",
    "6" : "Aground",
    "7" : "Engaged in Fishing",
    "8" : "Under way sailing",
    "9" : "Reserved for future amendment of Navigational Status for ships carrying DG, HS, or MP, IMO hazard or pollutant category A",
    "10" : "Reserved for future amendment of Navigational Status for ships carrying DG, HS or MP, IMO hazard or pollutant category B",
    "11" : "Reserved for future amendment of Navigational Status for ships carrying DG, HS or MP, IMO hazard or pollutant category C",
    "12" : "Reserved for future amendment of Navigational Status for ships carrying DG, HS or MP, IMO hazard or pollutant category D",
    "13" : "Reserved for future use",
    "14" : "AIS-SART (active); MOB-AIS; EPIRB-AIS",
    "15" : "undefined (default)"
}

app = Flask(__name__, static_folder=os.path.join(os.getcwd(), "templates/static"))
# Use an environment variable for your database URI, don't hard-code it.
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
db.init_app(app)

scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(
    func=delete_old_data,
    trigger=IntervalTrigger(days=1),
    id='delete_old_data_job',
    name='Delete old vessel data every day',
    replace_existing=True)

@app.route('/')
def index():
    return render_template('map.html')

@app.route('/data')
def data():
    vessel_data = VesselData.query.all()  # fetch all vessel data
    # convert data to JSON
    return jsonify([{
        'mmsi': data.mmsi,
        'name': data.shipname,
        'status': STATUS_DICT.get(data.navigationalstatus, 'Unknown status'),
        'lat': data.latitude,
        'lon': data.longitude,
    } for data in vessel_data])

if __name__ == "__main__":
    app.run(debug=True)

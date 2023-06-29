# Import the dependencies.
import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """Homepage and all available api routes"""
    return(
        f"Welcome to the homepage!<br/>"
        f"Here are the available routes: <br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start<br/>"
        f"/api/v1.0/temp/start/end"
)

@app.route("/api/v1.0/precipitation")
def precipitation():
    #create a session link
    session = Session(engine)
    
    #Query for precipitation analysis
    results = session.query(Measurement.date,Measurement.prcp).all()
    
    session.close()
    #convert query results from precipitation analysis
    all_prcp = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict['date'] = date
        prcp_dict['prcp'] = prcp
        all_prcp.append(prcp_dict)
        
    return jsonify(all_prcp)
    
    
@app.route("/api/v1.0/stations")
def station():
    session=Session(engine)
    
    #Query all the stations
    list_of_stations = session.query(Station.station,Station.name).all()
    
    session.close()
    
    #Convert the query results
    all_station = []
    for station, name in list_of_stations:
        station_dict = {}
        station_dict['station'] = station
        station_dict['name'] = name
        all_station.append(station_dict)
    
    return jsonify(all_station)

@app.route("/api/v1.0/tobs")
def tob():
    session=Session(engine)
    
    #Query all the observed temperatures
    recent_date  = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    recent_date_new_format = dt.date(2017,8,23)
    one_year_later = recent_date_new_format - dt.timedelta(days = 365)
    tob_date = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station=="USC00519281")\
.filter(Measurement.date>=one_year_later).all()
    
    session.close()
    
    #Convert the query results
    all_tob = []
    for date, tobs in tob_date:
        tob_dict = {}
        tob_dict['date'] = date
        tob_dict['tobs'] = tobs
        all_tob.append(tob_dict)
    
    return jsonify(all_tob)
    
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def start_end_stats(start=None, end=None):

    # Select statement
    stats= [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
     
        start = dt.datetime.strptime(start, "%m%d%Y")
        end_results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        session.close()

        temps = list(np.ravel(end_results))
        return jsonify(temps)

    start = dt.datetime.strptime(start, "%m%d%Y")
    end = dt.datetime.strptime(end, "%m%d%Y")

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()

    session.close()

    # Unravel results into a 1D array and convert to a list
    temps = list(np.ravel(results))
    return jsonify(temps=temps)
    #return jsonify(temps)

    # calculate TMIN, TAVG, TMAX with start and stop
    start = dt.datetime.strptime(start, "%m%d%Y")
    end = dt.datetime.strptime(end, "%m%d%Y")

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()

    session.close()

    # Unravel results into a 1D array and convert to a list
    temps = list(np.ravel(results))
    return jsonify(temps=temps)




if __name__ == '__main__':
    app.run(debug=True)

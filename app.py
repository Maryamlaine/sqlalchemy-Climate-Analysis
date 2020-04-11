# Design a Flask API based on the queries that you have just developed.
#################################################
# Import dependencies
#################################################
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import datetime as dt
import pandas as pd
import numpy as np
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement=Base.classes.measurement
Station=Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
# Home page
# List all routes that are available.
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Welcome to the weather API!<br/>"
        f"<br/>"
        f"Available Routes:<br/>"
        f"<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"<br/>"
        f"/api/v1.0/stations<br/>"
        f"<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
        f"<br/>"
        f"Note: Please put the dates in 'YYYY-MM-DD' format :) "
    )           
# Convert the query results to a dictionary using `date` as the key and `prcp` as the value.
@app.route("/api/v1.0/precipitation")
def precip_data():
    session = Session(engine)

    # Query
    past12mth_date= dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.date,Measurement.prcp).\
        filter(Measurement.date >=past12mth_date).all()

    session.close()
# Create a dictionary from the row data and append to a list of percipitation data
    results_dict = []
    for date, prcp in results:
        percip_dict = {}
        percip_dict["date"] = date
        percip_dict["prcp"] = prcp
        results_dict.append(percip_dict)
        
# Return the JSON representation of your dictionary.
    return jsonify(results_dict)


# Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def jsonified():
    session = Session(engine)
    # Query
    stations= session.query(Station.station).all()
    all_stations = list(np.ravel(stations))
    session.close()

    return jsonify(all_stations)

#  Query the dates and temperature observations of the most active station for the last year of data.

@app.route("/api/v1.0/tobs")
def temp_obs():
    session = Session(engine)
    past12mth_date= dt.date(2017, 8, 23) - dt.timedelta(days=365)
    temp_active = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station =="USC00519281").\
    filter(Measurement.date >= past12mth_date).order_by(Measurement.date.desc()).all()

    session.close()
# Create a dictionary from the row data and append to a list
    temp_list=[]
    temp_dict={}
    for temp in temp_active:
      temp_dict = {"date": temp[0], "tobs": temp[1]}
      temp_list.append(temp_dict)
 
# Return a JSON list of temperature observations (TOBS) for the previous year.
    
    return jsonify(temp_active)

    
@app.route("/api/v1.0/<start>")
def calc_temps(start):
    session = Session(engine)

    output = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).all()

    session.close()
    return jsonify(output)

@app.route("/api/v1.0/<start>/<end>")
def calc_temps_range(start, end):
    session = Session(engine)

    output = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    session.close()
    return jsonify(output) 
if __name__=="__main__":
    app.run(debug=True)    
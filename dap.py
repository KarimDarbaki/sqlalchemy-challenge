import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import pandas as pd 

#################################################
# Database Setup
#################################################

#engine = create_engine("sqlite:///Resources/hawaii.sqlite")
engine = create_engine("sqlite:///Resources/hawaii.sqlite",connect_args={'check_same_thread': False}, echo=False)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/Stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Convert the query results to a dictionary using date as the key and prcp as the value."""
    # Query all passengers
    results = session.query(Measurement.date, Measurement.prcp).order_by(Measurement.date.desc()).all()

    session.close()

    # # Convert list of tuples into normal list
    last_365 = dict(results)

    return jsonify(last_365)
   


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all passengers
    results_station = session.query(Station.station).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    station_listed = list(np.ravel(results_station))

    return jsonify(station_listed)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query the dates and temperature observations of the most active station for the last year of data.
    temps = session.query(func.max(Measurement.tobs),func.min(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.station=='USC00519281').all()
    session.close()

    # Return a JSON list of temperature observations (TOBS) for the previous year.
    lastyear_temps = list(np.ravel(temps))

    return jsonify(lastyear_temps)


@app.route("/api/v1.0/<start>")
def starter(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query the dates and temperature observations of the most active station for the last year of data.
    start_temp =  session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                 filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    # Return a JSON list of temperature observations (TOBS) for the previous year.
    temp_summary = list(np.ravel(start_temp))

    return jsonify(temp_summary)


if __name__ == '__main__':
    app.run(debug=True)
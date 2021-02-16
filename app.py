import numpy as np

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
Base.prepare(engine, reflect=True)

# Save reference to the table
measurements = Base.classes.measurement
stations = Base.classes.station

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
        f"<li>/api/v1.0/precipitation</li>"
        f"<li>/api/v1.0/stations</li>"
        f"<li>/api/v1.0/tobs</li>"
        f"<li>/api/v1.0/<start>/<end></li>"
    )

@app.route("/api/v1.0/precipitation")
def prcp():
    session = Session(engine)
    return { key:prcp for key, prcp in session.query(measurements.date, measurements.prcp).all() }

@app.route("/api/v1.0/stations")
def station():
    session = Session(engine)
    return { sta:name for sta, name in session.query(stations.station,stations.name).all() }

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    return { date:temp for date, temp in session.query(measurements.date,measurements.tobs).filter((measurements.station == 'USC00519281') & (measurements.date > '2016-08-22')).all() }

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def temps(start='2010-01-01', end='2017-08-23'):
    session = Session(engine)

    sel = [func.min(measurements.tobs),func.avg(measurements.tobs),func.max(measurements.tobs)]
    return jsonify(session.query(*sel).filter((measurements.date >= start) & (measurements.date <= end)).all())

if __name__ == '__main__':
    app.run(debug=True)

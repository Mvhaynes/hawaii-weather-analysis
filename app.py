from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import numpy as np

# Set up
app.Flask(__name__)
engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

# Home page: List available routes
@app.route('/')
def home():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>")
 
# Precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():

    # Query precipitation data
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()
    
    # Add each result as dictionary, append to list 
    prcp_data = []
    for precipitation, date in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = precipitation
        prcp_data.append(prcp_dict)

    return jsonify(prcp_data)

# Stations route
@app.route("/api/v1.0/stations")
def stations():

    # Query stations
    session = Session(engine)
    results = session.query(Station.station).all()
    sessionn.close()

    # Add results to dictionary
    stations = []
    for station in results:
        station_dict = {}
        station_dict['station'] = station
        stations.append(station_dict)
    
    return jsonify(stations)

# Temp observation route
@app.route('/api/v1.0/tobs')
    def tobs():

        # Query dates and temperatures for the most active station over the past year of data 
        session = Session(engine)

        # Find most recent date and convert to dt format 
        recent = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
        recent = recent[0]
        recent = dt.datetime.strptime(recent, '%Y-%m-%d')

        # Calculate one year ago 
        one_year = recent - dt.timedelta(days=365)

        # Find most active station 
        most_active = session.query(Measurement.station).group_by(Measurement.station).order_by(func.count(Measurement.id).desc()).first()

        # Query date and temps 
        results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.station == most_active).filter(Measurement.date > one_year).all()
        
        session.close()

if __name__ == "__main__":
    app.run(debug=True)


* `/api/v1.0/tobs`
  * Query the dates and temperature observations of the most active station for the last year of data.

  * Return a JSON list of temperature observations (TOBS) for the previous year.

* `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`

  * Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

  * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.

  * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.
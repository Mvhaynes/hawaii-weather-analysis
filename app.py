from flask import Flask, jsonify
from datetime import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


# Set up
app = Flask(__name__)
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
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
        f"/api/v1.0/(start)<br/>"
        f"/api/v1.0/(start)/(end)")
 
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
    session.close()

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

    # Return json list 
    most_active_prcp = []
    for date, prcp in results:
        active_dict = {}
        active_dict['date'] = date
        active_dict['prcp'] = prcp
        most_active_prcp.append(active_dict)
    return jsonify(most_active_prcp)

    session.close()

@app.route('/api/v1.0/<start>')
def start():
    start = dt.datetime.strptime(start, '%Y-%m-%d')
    # Query the database for: Min temp, Max temp, Avg temp
    session = Session(engine)
    result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
        .filter(Measurement.date >= start).all()
    
    # Add results to dictionaries and compile
    tobs = []
    for min_tob, avg_tob, max_tob in result:
        tob_dict = {}
        tob_dict['TMIN'] = min_tob
        tob_dict['TAVG'] = avg_tob
        tob_dict['TMAX'] = max_tob
        tobs.append(tob_dict)
    return jsonify(tobs)   

    session.close()

@app.route('/api/v1.0/<start>/<end>')
def start_stop():
    # Query the database for: Min temp, Max temp, Avg temp
    session = Session(engine)

    # Format query input
    start = dt.datetime.strptime(start, '%Y-%m-%d')
    end = dt.datetime.strptime(end, '%Y-%m-%d')

    result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
        .filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    # Add results to dictionaries and compile
    tobs = []
    for min_tob, avg_tob, max_tob in result:
        tob_dict = {}
        tob_dict['TMIN'] = min_tob
        tob_dict['TAVG'] = avg_tob
        tob_dict['TMAX'] = max_tob
        tobs.append(tob_dict)
    return jsonify(tobs)   

    session.close()

# Enable execution
if __name__ == "__main__":
    app.run(debug=True)
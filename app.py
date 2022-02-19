# Import dependencies
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.types import Date
from sqlalchemy.orm import Session, scoped_session, sessionmaker
from sqlalchemy import func
from flask import Flask, jsonify


#set up base
Base = declarative_base()

#create class for measurement table
class Measurement(Base):
    __tablename__ = "measurement"
    
    id = Column(Integer, primary_key=True)
    station = Column(String)
    date = Column(Date)
    prcp = Column(Float)
    tobs = Column(Float)


#create class for station table
class Station(Base):
    __tablename__ = "station"
    
    id = Column(Integer, primary_key=True)
    station = Column(String)
    name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    elevation =  Column(Float)


# create engine and session to link to the database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
conn = engine.connect()
session = scoped_session(sessionmaker(bind=engine))


# establish app
app = Flask(__name__)


# create home page route
@app.route("/")
def main():
    return (
        f"Welcome to the Climate App Home Page!<br>"
        f"Available Routes Below:<br>"
        f"Precipitation measurement over the last 12 months: /api/v1.0/precipitation<br>"
        f"A list of stations and their respective station numbers: /api/v1.0/stations<br>"
        f"Temperature observations at the most active station over the previous 12 months: /api/v1.0/tobs<br>"
        f"Enter a start date (yyyy-mm-dd) to retrieve the minimum, maximum, and average temperatures for all dates after the specified date: /api/v1.0/<start><br>"
        f"Enter both a start and end date (yyyy-mm-dd) to retrieve the minimum, maximum, and average temperatures for that date range: /api/v1.0/<start>/<end><br>"
    )


# create precipitation route of last 12 months of precipitation data
#@app.route("/api/v1.0/precipitation")
#def precip():

    #recent_prcp = session.query(str(Measurement.date), Measurement.prcp)\
    #.filter(str(Measurement.date) > '2016-08-22')\
    #.filter(str(Measurement.date) <= '2017-08-23')\
    #.order_by(str(Measurement.date)).all()

import datetime as dt

@app.route("/api/v1.0/precipitation")
def precip():
    prev_year = dt.date(2016, 8, 22) 
    current_year = dt.date(2017, 8, 23) 
    recent_prcp = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).\
        filter(Measurement.date < current_year).all()

    precip = {str(date): prcp for date, prcp in recent_prcp}
    return jsonify(precip)

    # convert results to a dictionary with date as key and prcp as value
   # prcp_dict = dict(recent_prcp)

    # return json list of dictionary
    #return jsonify(prcp_dict)


# create station route of a list of the stations in the dataset
@app.route("/api/v1.0/stations")
def stations():

    stations = session.query(Station.name, Station.station).all()

    # convert results to a dict
    stations_dict = dict(stations)

    # return json list of dict 
    return jsonify(stations_dict)


# create tobs route of temp observations for most active station over last 12 months
#@app.route("/api/v1.0/tobs")
#def tobs():

    #tobs_station = session.query(str(Measurement.date), Measurement.tobs)\
    #.filter(str(Measurement.date) > '2016-08-23')\
    #.filter(str(Measurement.date) <= '2017-08-23')\
    #.filter(str(Measurement.station) == "USC00519281")\
    #.order_by(str(Measurement.date)).all()

    # convert results to dict
    #tobs_dict = dict(tobs_station)

    # return json list of dict
    #return jsonify(tobs_dict)


@app.route("/api/v1.0/tobs")
def tobs():
    prev_year = dt.date(2016, 8, 22) 
    current_year = dt.date(2017, 8, 23) 
    recent_prcp = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).\
        filter(Measurement.date < current_year).all()

    precip = {str(date): prcp for date, prcp in recent_prcp}
    return jsonify(precip)

# create start and start/end route
# min, average, and max temps for a given date range
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def start_date(start, end=None):

    q = session.query(str(func.min(Measurement.tobs)), str(func.max(Measurement.tobs)), str(func.round(func.avg(Measurement.tobs))))

    if start:
        q = q.filter(Measurement.date >= start)

    if end:
        q = q.filter(Measurement.date <= end)

    # convert results into a dictionary

    results = q.all()[0]

    keys = ["Min Temp", "Max Temp", "Avg Temp"]

    temp_dict = {keys[i]: results[i] for i in range(len(keys))}

    return jsonify(temp_dict)


if __name__ == "__main__":
    app.run(debug=True)

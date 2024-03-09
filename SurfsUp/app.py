# Import the dependencies.
from flask import Flask, jsonify
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
#################################################
# Database Setup
# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
#################################################
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
app = Flask(__name__)
#################################################

#################################################
# Flask Routes
@app.route("/")
def main():
    return (
        f"Welcome to the Climate App Home Page!<br>"
        f"Available Routes:<br>"
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"To return all data after a specific date, replace 'start' with desired date in yyyy-mm-dd format.<br>"
        f"/api/v1.0/start<br>"
        f"To return all data between specific dates, replace 'start' and 'end' with desired date range in yyyy-mm-dd format.<br>"
        f"/api/v1.0/start>/<end><br>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    #create session
    session = Session(engine)
 #Precipitation data from last 12 months from the most recent date from measurement table
    prev_year = dt.date(2017,8,23) - dt.timedelta(days = 365)

    results = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >=prev_year.\order_by(Measurement.date.desc()).all()

    session.close()

#create a dictionary from the data
    prcp_data = []
    for date, prcp in prcp_data:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp_list.append(prcp_dict)
    return jsonify(precip_data)

@app.route("/api/v1.0/stations")
def station():
    #create session
    session = Session(engine)

    #query station data from the station table
    station_data = session.query(Station.station).all()

   #close session                  
    session.close()

    #convert the list of tuples into normal list
    station_list = list(np.ravel(station_data))

    #return a json list of station from the table
     return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    #create session
    session = Session(engine)

    # query the last date one year from the table.
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days = 365)
    main_station = 'USC00519281'

    prev_year_temp = session.query(Measurement.date, Measurement.tobs).\
           filter(Measurement.station == main_station.\
                  filter(Measurement.date >= prev_year).all()
 

    session.close()

    temp_data = []
    for date, tobs in prev_year_temp:
        temp_dict = {}
        temp_dict["date"] = date
        temp_dict["temperature"] = tobs
        temp_data.append(temp_dict)

    #return a json list of temperature from the table
    return jsonify(temp_data)
                  
@app.route("/api/v1.0/<start>")                 
def start_date(start):
    
    start_date=dt.datetime.strptime(start, "%Y-%m-%d")

    results= session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))
                  \.filter(Measurement.date>=start_date\.all()

    #dictionary
    temp_dict={'TMIN':results[0][0], 'TVAG': round(results[0][1],2),'TMAX':results[0][2]}

    #json dictionary
    return jsonify(temp_dict)
                           
@app.route("/api/v1.0/start>/<end>")
def start_end_date(start, end):
    #TMIN, TAVG, and TMAX for dates between the start and end dates
    start_date = dt.datetime.strptime(start, "%Y-%m-%d")
    end_date = dt.datetime.strptime(end, "%Y-%m-%d")
    results = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs))\
        .filter(Measurement.date>=start_date)\
        .filter(Measurement.date>=end_date)\
        .all()

    # Create dictionary with the results
    temp_dict = {'TMIN':results[0][0], 'TVAG': round(results[0][1],2), 'TMAX': results[0][2]}

    # Return the JSON representation of the dictionary
    return jsonify(temp_dict)
if __name__ =='__main__':
    app.run()
                              

#################################################






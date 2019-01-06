#!/usr/bin/env python
# coding: utf-8

# In[1]:


import datetime as dt
import pandas as pd
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


# In[2]:


engine = create_engine("sqlite:///Resources/hawaii.sqlite")


# In[3]:


Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(bind=engine)


# In[4]:


app = Flask(__name__)


# In[5]:


#Home Page
@app.route("/")
def home():
    print("Hello!")
    return "Welcome to the Surfs Up! Weather API!"


# In[6]:


#List of All Available Routes
@app.route("/Welcome")
def welcome ():
    return (
        f"Welcome to the Surfs Up! API<br>"
        f"Available Routes:<br>"
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/<start><br>"
        f"/api/v1.0<start>/<end><br>"
    )


# In[7]:


#Precipitation Data over Last 12 Months
@app.route("/api/v1.0/precipitation")
def precipitation():
    results = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date >= "2016-08-23").all()
    precip_year = list(np.ravel(results))
    precip_data = []
    for precipitation in results:
        row = {}
        row[Measurement.date] = row[Measurement.prcp]
        year_prcp.append(row)
    return jsonify(precip_year)


# In[8]:


#Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Stations.station).all()
    station_list = list(np.ravel(results))
    return jsonify(station_list)


# In[9]:


#Return a JSON list of Temperature Observations (tobs) for the previous year
@app.route("/api/v1.0/tobs")
def temperature():
    tobs_data = []
    results = session.query(Measurement.tobs).filter(Measurement.date >= "2016-08-23").all()
    tobs_year = list(np.ravel(results))
    return jsonify(tobs_year)


# In[10]:


#Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
@app.route("/api/v1.0/<start>")
def start_temp(start_date):
    start_time = []
    min_temp= session.query(func.min(Measurement.tobs)).filter(Measurement.date == start_date).all()
    max_temp = session.query(func.max(Measurement.tobs)).filter(Measurement.date == start_date).all()
    mean_temp = session.query(func.avg(Measurement.tobs)).filter(Measurement.date == start_date).all()
    start_time = list(np.ravel(min_temp,max_temp, mean_temp))
    return jsonify(start_time)

#When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date
def greater_equal_start_temp(start_date):
    start_greater_time = []
    min_temp = session.query(func.min(Measurement.tobs)).filter(Measurement.date >= start_date).all()
    max_temp = session.query(func.max(Measurement.tobs)).filter(Measurement.date >= start_date).all()
    mean_temp = session.query(func.avg(Measurement.tobs)).filter(Measurement.date >= start_date).all()
    start_greater_time = list(np.ravel(min_temp, max_temp, mean_temp))
    return jsonify(start_greater_time)


# In[11]:


#Equal to the End Date
@app.route("/api/v1.0/<start>/<end>")
def start_end_time(start_date, end_date):
    start_end_time = []
    min_temp = session.query(func.min(Measurement.tobs)).filter(Measurement.date == start_date, Measurement.date == end_date).all()
    max_temp = session.query(func.max(Measurement.tobs)).filter(Measurement.date == start_date, Measurement.date == end_date).all()
    mean_temp = session.query(func.avg(Measurement.tobs)).filter(Measurement.date == start_date, Measurement.date == end_date).all()
    start_end_time = list(np.ravel(min_temp, max_temp, mean_temp))
    return jsonify(start_end_time)

#When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive
def start_end_between(start_date, end_date):
    between_time = []
    results_min = session.query(func.min(Measurement.tobs)).filter(Measurement.date >= start_date, Measurement.date >= end_date).all()
    results_max = session.query(func.max(Measurement.tobs)).filter(Measurement.date >= start_date, Measurement.date >= end_date).all()
    results_avg = session.query(func.avg(Measurement.tobs)).filter(Measurement.date >= start_date, Measurement.date >= end_date).all()
    between_time = list(np.ravel(min_temp, max_temp, mean_temp))
    return jsonify(between_time)

if __name__ == '__main__':
    app.run(debug=True)


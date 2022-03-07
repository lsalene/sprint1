# Leira Salene
# Sprint 1
# 1785752

import hashlib
import mysql.connector
from mysql.connector import Error
# importing the queries to connect vscode to mysql
from sql import create_connection
from sql import execute_query
from sql import execute_read_query
# import flask library from python
import flask
# import jsonify to make the crub operations execute in JSON format
from flask import jsonify
from flask import request, make_response

# connection to aws
conn = create_connection('cis3368.cjryivjdivtd.us-east-2.rds.amazonaws.com',  'admin', 'AWS!cis3368', 'cis3368db')

# setting up an application name
app = flask.Flask(__name__) #sets up the application
app.config["DEBUG"] = True #allow to show errors in browser

masterPassword = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"
masterUsername = 'username1'
validokens = {
    "100", "200", "300", "400"
}

# route to authenticate with username and password against a dataset (ideally from database and also hashed, not clear strings for passwords)
# test in postman by creating header parameters 'username' and 'password' and pass in credentials
# default url to force user to login before continuing to make changes to tables
@app.route('/authenticatedroute', methods=['GET'])
def auth_example():
    if request.authorization:
        encoded = request.authorization.password.encode()  # unicode encoding
        hashedResult = hashlib.sha256(encoded)  # hashing
        if request.authorization.username == masterUsername and hashedResult.hexdigest() == masterPassword:
            return '<h1> WE ARE ALLOWED TO BE HERE </h1>'
    return make_response('COULD NOT VERIFY!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})


# home url that returns canada trip when executed
@app.route('/home', methods=['GET'])
def home():
    return "<h1> Vacation Destination </h1>"

## GET: all destinations and trips
# retrieves all of the data from the destinations table
@app.route('/api/destination/all', methods=['GET'])
def alldestination():
    request_data = request.get_json()
    destsql = "SELECT * FROM destination"
    destinations = execute_read_query(connection, destsql)
    return jsonify(destinations)

# retrieves the data from the trips table and executes it in json format using the return line
@app.route('/api/trips/all', methods=['GET'])
def alltrip():
    request_data = request.get_json()
    tripsql = "SELECT * FROM trip"
    trips = execute_read_query(connection, tripsql)
    return jsonify(trips)

## GET: specific destination and trip
# retrieves the data asked for from the destination table
@app.route('/api/destinationid', methods=['GET'])
def destinationid():
    request_data = request.get_json()
    destinationid = request_data['id']
    destsql = "SELECT * FROM destination WHERE id = '%s'"%(destinationid)
    destinations = execute_read_query (conn, destsql)
    return jsonify(destinations)

# retrieves data asked for from the trips table
@app.route('/api/tripid', methods=['GET'])
def tripid():
    request_data = request.get_json()
    tripid = request_data['id']
    tripsql = "SELECT * FROM trip WHERE id = '%s'" % (tripid)
    trips = execute_read_query (conn, tripsql)
    return jsonify(trips)

## POST: add destinations and trips into the tables
# add destination into the destination table
@app.route('/api/destination/add', methods=['POST'])
def destination(): 
    request_data = request.get_json()
    country = request_data['country']
    city = request_data['city']
    ss = request_data['sightseeing']
    destsql = "INSERT INTO destination (country, city, sightseeing) VALUES ('%s', '%s', '%s')" %(country, city, ss)
    execute_query(conn, destsql)
    return 'destination added successfully'

# add a trip 
@app.route('/api/trip/add', methods=['POST'])
def trip(): 
    request_data = request.get_json()
    did = request_data['destinationid']
    transportation = request_data['transportation']
    sd = request_data['startdate']
    ed = request_data['enddate']
    tripsql = "INSERT INTO trip (destinationid, transportation, startdate, enddate) VALUES ('%s', '%s', '%s', '%s)" %(destinationid, transportation, startdate, enddate)
    execute_query(conn, tripsql)
    return 'trip added successfully'

## DELETE: delete trips or destinations from the sql tables
# delete destination of choice by id 
@app.route('/api/destination/delete', methods=['DELETE'])
def deldestination():
    request_data = request.get_json()
    did = request_data['id']
    destsql = "DELETE FROM destination WHERE id = '%s'" % (did)
    execute_query(connection, destsql)
    return "destination successfully deleted"

# delete trip of choice by specifying id
@app.route('/api/destination/delete', methods=['DELETE'])
def deltrip():
    request_data = request.get_json()
    tid = request_data['id']
    tripsql = "DELETE FROM trip WHERE id = '%s'" % (tid)
    execute_query(connection, tripsql)
    return "trip successfully deleted"

## PUT: update existing information on tables destination and trip
# update the destination information based on the selected destination's id
@app.route('/api/destination/delete', methods=['PUT'])
def upddestination():
    request_data = request.get_json()
    did = request_data['id']
    country = request_data['country']
    city = request_data['city']
    ss = request_data['sightseeing']
    destsql = "UPDATE destination SET  country = '%s', city = '%s', sightseeing = '%s' WHERE id = '%s'" % (country, city, ss, did)
    execute_query(connection, destsql)
    return "destination successfully updated"

# update the destination information based on the selected destination's id
@app.route('/api/trip/delete', methods=['PUT'])
def updtrip():
    request_data = request.get_json()
    tid = request_data['id']
    did = request_data['destinationid']
    transportation = request_data['transportation']
    sd = request_data['startdate']
    ed = request_data['enddate']
    tripsql = "UPDATE trip SET destinationid = '%s', transportation = '%s', startdate = '%s', enddate = '%s' WHERE id = '%s'" % (did, transportation, sd, ed, tid)
    execute_query(connection, tripsql)
    return "trip successfully updated"


app.run()
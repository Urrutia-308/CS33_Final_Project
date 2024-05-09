#app.py file
from flask import Flask, request, jsonify
from flask_cors import CORS 
from models import connectToDB
import mysql.connector

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains on all routes

@app.route('/')
def home():
    return "Welcome! :)", 200

@app.route('/createSchedule', methods=['POST'])
def create_schedule():
    connection = connectToDB()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    schedule_title = request.json.get('title')
    result, error, status_code = create_schedule_logic(schedule_title, connection)
    if error:
        return jsonify({'error': error}), status_code
    return jsonify(result), status_code

def create_schedule_logic(schedule_title, db_connection):
    if not schedule_title:
        return None, 'No title provided', 400

    try:
        cursor = db_connection.cursor()
        sql = "INSERT INTO Scheduler.schedules (title) VALUES (%s)"
        cursor.execute(sql, (schedule_title,))
        db_connection.commit()
        schedule_id = cursor.lastrowid
        cursor.close()
        return {'message': 'Schedule created successfully', 'scheduleID': schedule_id}, None, 201
    except mysql.connector.Error as err:
        return None, str(err), 500

@app.route('/getSchedules', methods=['GET'])
def get_schedules():
    connection = connectToDB()
    schedules, error, status_code = get_schedules_logic(connection)
    if error:
        return jsonify({'error': error}), status_code
    return jsonify(schedules), status_code


def get_schedules_logic(db_connection):
    if not db_connection:
        return None, 'Database connection failed', 500

    try:
        cursor = db_connection.cursor()
        cursor.execute("SELECT scheduleID, title FROM Scheduler.schedules")
        schedules = cursor.fetchall()
        cursor.close()
        # Convert the fetched schedules to a list of dicts
        schedule_list = [{'id': schedule[0], 'title': schedule[1]} for schedule in schedules]
        return schedule_list, None, 200
    except mysql.connector.Error as err:
        return None, str(err), 500

    
@app.route('/deleteSchedule/<int:schedule_id>', methods=['DELETE'])
def delete_schedule(schedule_id):
    connection = connectToDB()
    result, error, status_code = delete_schedule_logic(schedule_id, connection)
    if error:
        return jsonify({'error': error}), status_code
    return jsonify(result), status_code


def delete_schedule_logic(schedule_id, db_connection):
    if not db_connection:
        return None, 'Database connection failed', 500

    try:
        cursor = db_connection.cursor()
        cursor.execute("DELETE FROM Scheduler.schedules WHERE scheduleID = %s", (schedule_id,))
        db_connection.commit()
        deleted_count = cursor.rowcount
        cursor.close()
        if deleted_count == 0:
            return None, 'No schedule found with the given ID', 404
        return {'message': 'Schedule deleted successfully'}, None, 200
    except mysql.connector.Error as err:
        return None, str(err), 500


@app.route('/addEvent', methods=['POST'])
def add_event():
    connection = connectToDB()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500

    data = request.get_json()
    result, error, status_code = add_event_logic(data, connection)
    if error:
        return jsonify({'error': error}), status_code
    return jsonify(result), status_code


def add_event_logic(data, db_connection):
    required_fields = ['scheduleID', 'description', 'color', 'startTime', 'endTime', 'daysOfWeek']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return None, f"Missing required fields: {', '.join(missing_fields)}", 400

    try:
        cursor = db_connection.cursor()
        sql = "INSERT INTO events (scheduleID, description, color, startTime, endTime, daysOfWeek) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (data['scheduleID'], data['description'], data['color'], data['startTime'], data['endTime'], ','.join(data['daysOfWeek'])))
        db_connection.commit()
        event_id = cursor.lastrowid
        cursor.close()
        return {'message': 'Event added successfully', 'eventID': event_id}, None, 201
    except mysql.connector.Error as err:
        return None, str(err), 500

    
@app.route('/deleteEvent/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    connection = connectToDB()
    result, error, status_code = delete_event_logic(event_id, connection)
    if error:
        return jsonify({'error': error}), status_code
    return jsonify(result), status_code

def delete_event_logic(event_id, db_connection):
    if not db_connection:
        return None, 'Database connection failed', 500

    try:
        cursor = db_connection.cursor()
        cursor.execute("DELETE FROM events WHERE eventID = %s", (event_id,))
        db_connection.commit()
        affected_rows = cursor.rowcount
        cursor.close()
        if affected_rows == 0:
            return None, 'No event found with the given ID', 404
        return {'message': 'Event deleted successfully'}, None, 200
    except mysql.connector.Error as err:
        return None, str(err), 500


    

@app.route('/getEvents/<int:scheduleID>', methods=['GET'])
def get_events(scheduleID):
    connection = connectToDB()
    events, error, status_code = get_events_logic(scheduleID, connection)
    if error:
        return jsonify({'error': error}), status_code
    return jsonify(events), status_code

def get_events_logic(scheduleID, db_connection):
    if not db_connection:
        return None, 'Database connection failed', 500

    try:
        cursor = db_connection.cursor()
        cursor.execute("SELECT eventID, description, color, startTime, endTime, daysOfWeek FROM events WHERE scheduleID = %s", (scheduleID,))
        events = cursor.fetchall()
        cursor.close()
        events_list = [
            {'eventID': event[0],
             'description': event[1],
             'color': event[2],
             'startTime': str(event[3]),
             'endTime': str(event[4]),
             'daysOfWeek': event[5].split(',')
             }
            for event in events]
        return events_list, None, 200
    except mysql.connector.Error as err:
        return None, str(err), 500

    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

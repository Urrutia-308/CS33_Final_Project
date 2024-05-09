#test_units file
import pytest
from unittest.mock import MagicMock
from app import create_schedule_logic, get_schedules_logic, delete_schedule_logic, add_event_logic, delete_event_logic, get_events_logic
import mysql.connector

def test_create_schedule_success():
    db_connection = MagicMock()
    cursor = db_connection.cursor.return_value
    cursor.lastrowid = 1 
    
    data, error, status_code = create_schedule_logic('Team Meeting', db_connection)
    
    assert error is None
    assert status_code == 201
    assert 'message' in data

def test_create_schedule_no_title():
    db_connection = MagicMock()  #no operations should be called on this

    data, error, status_code = create_schedule_logic('', db_connection)
    
    assert data is None
    assert error == 'No title provided'
    assert status_code == 400

def test_create_schedule_db_error():
    db_connection = MagicMock()
    cursor = db_connection.cursor.return_value
    cursor.execute.side_effect = mysql.connector.Error("DB error")

    data, error, status_code = create_schedule_logic('Team Meeting', db_connection)
    
    assert data is None
    assert 'DB error' in error
    assert status_code == 500

def test_get_schedules_success():
    db_connection = MagicMock()
    cursor = db_connection.cursor.return_value
    cursor.fetchall.return_value = [(1, 'Schedule A'), (2, 'Schedule B')]
    
    schedules, error, status_code = get_schedules_logic(db_connection)
    
    assert error is None
    assert status_code == 200
    assert isinstance(schedules, list)
    assert schedules[0]['id'] == 1
    assert schedules[0]['title'] == 'Schedule A'

def test_get_schedules_db_failure():
    db_connection = MagicMock()
    db_connection.cursor.side_effect = mysql.connector.Error("DB error")
    
    schedules, error, status_code = get_schedules_logic(db_connection)
    
    assert schedules is None
    assert 'DB error' in error
    assert status_code == 500

def test_get_schedules_no_connection():
    schedules, error, status_code = get_schedules_logic(None)
    
    assert schedules is None
    assert 'Database connection failed' == error
    assert status_code == 500

def test_delete_schedule_success():
    db_connection = MagicMock()
    cursor = db_connection.cursor.return_value
    cursor.rowcount = 1  

    result, error, status_code = delete_schedule_logic(1, db_connection)
    
    assert error is None
    assert status_code == 200
    assert result['message'] == 'Schedule deleted successfully'

def test_delete_schedule_not_found():
    db_connection = MagicMock()
    cursor = db_connection.cursor.return_value
    cursor.rowcount = 0  
    
    result, error, status_code = delete_schedule_logic(1, db_connection)
    
    assert result is None
    assert 'No schedule found with the given ID' == error
    assert status_code == 404

def test_delete_schedule_db_error():
    db_connection = MagicMock()
    cursor = db_connection.cursor.return_value
    cursor.execute.side_effect = mysql.connector.Error("DB error")
    
    result, error, status_code = delete_schedule_logic(1, db_connection)
    
    assert result is None
    assert 'DB error' in error
    assert status_code == 500

def test_add_event_success():
    db_connection = MagicMock()
    cursor = db_connection.cursor.return_value
    cursor.lastrowid = 101  

    event_data = {
        'scheduleID': 1,
        'description': 'Team Meeting',
        'color': '#0000FF',
        'startTime': '10:00',
        'endTime': '11:00',
        'daysOfWeek': ['Monday', 'Wednesday']
    }
    
    result, error, status_code = add_event_logic(event_data, db_connection)
    
    assert error is None
    assert status_code == 201
    assert result['message'] == 'Event added successfully'
    assert result['eventID'] == 101

def test_add_event_missing_fields():
    db_connection = MagicMock()

    #data simulating a request with missing fields
    event_data = {
        'description': 'Team Meeting',
        'color': '#0000FF'
    }
    
    result, error, status_code = add_event_logic(event_data, db_connection)
    
    assert result is None
    assert 'Missing required fields' in error
    assert 'scheduleID' in error
    assert status_code == 400

def test_add_event_db_error():
    db_connection = MagicMock()
    cursor = db_connection.cursor.return_value
    cursor.execute.side_effect = mysql.connector.Error("DB error")
    
    event_data = {
        'scheduleID': 1,
        'description': 'Team Meeting',
        'color': '#0000FF',
        'startTime': '10:00',
        'endTime': '11:00',
        'daysOfWeek': ['Monday', 'Wednesday']
    }
    
    result, error, status_code = add_event_logic(event_data, db_connection)

    assert result is None
    assert 'DB error' in error
    assert status_code == 500

def test_delete_event_success():
    db_connection = MagicMock()
    cursor = db_connection.cursor.return_value
    cursor.rowcount = 1  

    result, error, status_code = delete_event_logic(1, db_connection)
    
    assert error is None
    assert status_code == 200
    assert result['message'] == 'Event deleted successfully'

def test_delete_event_not_found():

    db_connection = MagicMock()
    cursor = db_connection.cursor.return_value
    cursor.rowcount = 0  # Simulate no rows deleted

    result, error, status_code = delete_event_logic(1, db_connection)
    
    assert result is None
    assert 'No event found with the given ID' == error
    assert status_code == 404

def test_delete_event_db_error():
    db_connection = MagicMock()
    cursor = db_connection.cursor.return_value
    cursor.execute.side_effect = mysql.connector.Error("DB error")

    result, error, status_code = delete_event_logic(1, db_connection)

    assert result is None
    assert 'DB error' in error
    assert status_code == 500

def test_get_events_success():
    db_connection = MagicMock()
    cursor = db_connection.cursor.return_value
    cursor.fetchall.return_value = [
        (1, 'Meeting', '#FF0000', '10:00', '11:00', 'Monday,Tuesday'),
        (2, 'Review', '#00FF00', '12:00', '13:00', 'Wednesday')
    ]

    events, error, status_code = get_events_logic(1, db_connection)
    
    assert error is None
    assert status_code == 200
    assert len(events) == 2
    assert events[0]['description'] == 'Meeting'

def test_get_events_no_connection():
    events, error, status_code = get_events_logic(1, None)
    
    assert events is None
    assert 'Database connection failed' == error
    assert status_code == 500

def test_get_events_db_error():
    db_connection = MagicMock()
    cursor = db_connection.cursor.return_value
    cursor.execute.side_effect = mysql.connector.Error("DB error")
    
    events, error, status_code = get_events_logic(1, db_connection)

    assert events is None
    assert 'DB error' in error
    assert status_code == 500

if __name__ == "__main__":
    pytest.main()

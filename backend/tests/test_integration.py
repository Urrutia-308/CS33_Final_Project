#test_integrations.py
from unittest.mock import patch
from flask_testing import TestCase
from app import app
from unittest.mock import patch, MagicMock

class TestFlaskApi(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        return app
    
    @patch('models.connectToDB')
    def test_create_schedule_success(self, mock_db):
        mock_conn = mock_db.return_value
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.lastrowid = 1  # Mock the ID returned after insertion
        response = self.client.post('/createSchedule', json={'title': 'Team Meeting'})
        assert response.status_code == 201
        assert 'Schedule created successfully' in response.json['message']

    @patch('models.connectToDB')
    def test_add_event_missing_fields(self, mock_db):
        event_data = {
            'scheduleID': 4,
            'color': '#000000',
            'startTime': '10:00:00',
            'endTime': '11:00:00',
            'daysOfWeek': ''
        }
        response = self.client.post('/addEvent', json=event_data)
        assert response.status_code == 400
        assert 'error' in response.json
        assert 'Missing required fields' in response.json['error']
        assert 'description' in response.json['error']

    

    @patch('app.get_schedules_logic')
    def test_get_schedules_success(self, mock_get_schedules_logic):
        # Mock the return value of get_schedules_logic
        mock_schedules = [
            {'id': 1, 'title': 'Team Meeting'},
            {'id': 2, 'title': 'Project Review'}
        ]
        mock_get_schedules_logic.return_value = (mock_schedules, None, 200)

        response = self.client.get('/getSchedules')
        assert response.status_code == 200
        assert len(response.json) == 2
        assert response.json == mock_schedules


    def test_create_schedule_no_title(self):
        """Test creating a schedule without a title to ensure it returns 400 error."""
        response = self.client.post('/createSchedule', json={})
        assert response.status_code == 400
        assert 'No title provided' in response.json['error']


    @patch('models.connectToDB')
    def test_delete_schedule_not_found(self, mock_db):
        mock_conn = mock_db.return_value
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.rowcount = 0

        response = self.client.delete('/deleteSchedule/1')
        assert response.status_code == 404
        assert 'No schedule found with the given ID' in response.json['error']



    """ @patch('models.connectToDB')
    def test_delete_event_success(self, mock_db):
        mock_conn = mock_db.return_value
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.rowcount = 1

        response = self.client.delete('/deleteEvent/80')
        assert response.status_code == 200
        assert 'Event deleted successfully' in response.json['message'] """
    
    @patch('app.delete_event_logic')
    def test_delete_event_success(self, mock_delete_event_logic):
        mock_delete_event_logic.return_value = ({'message': 'Event deleted successfully'}, None, 200)

        response = self.client.delete('/deleteEvent/80')
        assert response.status_code == 200
        assert 'Event deleted successfully' in response.json['message']

        mock_delete_event_logic.assert_called_once_with(80, mock_delete_event_logic.call_args[0][1])

    @patch('models.connectToDB')
    def test_delete_event_not_found(self, mock_db):
        mock_conn = mock_db.return_value
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.execute.return_value = None

        #set the rowcount to 0 to simulate no rows affected
        mock_cursor.rowcount = 0
        response = self.client.delete('/deleteEvent/1')

        assert response.status_code == 404
        assert 'No event found with the given ID' in response.json['error']

    @patch('models.connectToDB')
    def test_get_events_success(self, mock_db):
        mock_conn = mock_db.return_value
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.fetchall.return_value = [
            (40, 'My Event', '#fa0000', '10:00:00', '11:00:00', 'Tuesday,Thursday')
        ]

        response = self.client.get('/getEvents/40')
        assert response.status_code == 200
        assert len(response.json) == 1
        assert response.json[0]['description'] == 'My Event'

if __name__ == "__main__":
    pytest.main()

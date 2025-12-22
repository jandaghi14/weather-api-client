import pytest
from unittest.mock import patch, Mock
import client  # your file name
import database as db
from datetime import datetime, timedelta
import requests

# Test 1: API call when no cache
def test_get_weather_no_cache():
    """Test fetching from API when cache is empty"""
    with patch('client.db.chech_cache') as mock_cache, \
         patch('client.requests.get') as mock_get:
        
        # Setup mocks
        mock_cache.return_value = None  # No cache
        mock_get.return_value.json.return_value = {
            'main': {'temp': 290, 'humidity': 65},
            'weather': [{'description': 'clear sky'}]
        }
        
        # We also need to mock db.add_weather so it doesn't hit real DB
        with patch('client.db.add_weather'):
            result = client.get_weather("london")
        
        # Verify
        assert result[0] == "london"
        assert result[1] == 290
        mock_get.assert_called_once()  # API was called
def test_get_weather_from_cache():
    recent_time = (datetime.now()- timedelta(seconds=30)).strftime("%d/%m/%Y, %H:%M:%S")
    with patch('client.db.chech_cache') as mock_cach , \
         patch('client.requests.get') as mock_get:
        mock_cach.return_value = ('tehran', 280.98, 39, 'broken clouds', recent_time)
        result = client.get_weather('tehran')
        assert result[0] == 'tehran'
        assert result[2] == 39 
        mock_get.assert_not_called()
        
def test_connection_error():
    with patch('client.db.chech_cache') as mock_cache,\
        patch('client.requests.get') as mock_get:
            mock_cache.return_value = None
            mock_get.side_effect = requests.ConnectionError("Network error")
            result = client.get_weather('tehran')
            assert "error" in result
            assert mock_get.call_count == 3

def test_old_cache():
    recent_time = (datetime.now() - timedelta(seconds=65)).strftime("%d/%m/%Y, %H:%M:%S")
    with patch('client.db.chech_cache') as mock_cache, \
        patch('client.requests.get') as mock_get:
            mock_cache.return_value = ('tehran', 280.98, 39, 'broken clouds', recent_time)
            mock_get.return_value.json.return_value = {"main":{"temp" : 85 , "humidity" : "jooje"}, "weather" : [{"description" : "wow such a description"}]}
            with patch("client.db.update_cache_weather"):
                result = client.get_weather("tehran")
            assert result[1] == 85
            assert result[2] == "jooje"
            mock_get.assert_called_once()
            
def test_invalid_city():
    result = client.get_weather("rasht")
    assert "You have to insert the latitude and longitude of city" in result
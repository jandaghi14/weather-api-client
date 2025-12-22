# Weather API Client with Caching

Day 58 of Python Learning - API client with retry logic and intelligent caching.

## Features

- **Weather API Integration**: Fetch weather data from OpenWeatherMap
- **Retry Decorator**: Automatic retry with exponential backoff (3 attempts)
- **Smart Caching**: SQLite cache with 1-minute TTL
  - Fresh data (< 1 minute) → Read from cache
  - Stale data (> 1 minute) → Fetch from API and update cache
- **Error Handling**: Graceful handling of network failures
- **Comprehensive Tests**: 5 tests with mocking (unittest.mock)

## Project Structure
```
.
├── client.py           # Main weather client with retry logic
├── database.py         # SQLite cache operations
├── test_client.py      # Test suite with mocks
├── cache.db            # SQLite database (auto-created)
└── README.md
```

## How It Works

### Cache Logic Flow

1. **Check cache** for city data
2. **If no cache** → Fetch from API → Save to database
3. **If cache exists:**
   - **< 1 minute old** → Return cached data (no API call)
   - **> 1 minute old** → Fetch fresh data → Update cache

### Retry Decorator
```python
@retry
def get_weather(city):
    # Automatically retries on ConnectionError
    # Waits: 1s, 2s, 4s (exponential backoff)
```

## Supported Cities

Currently supports:
- London
- Tehran

(Add more in `cooardintaes()` function)

## Setup

1. **Install dependencies:**
```bash
pip install requests pytest
```

2. **Get API key:**
   - Sign up at [OpenWeatherMap](https://openweathermap.org/)
   - Replace `API_Key` in `client.py` with your key

3. **Run tests:**
```bash
pytest test_client.py -v
```

## Usage
```python
from client import get_weather

# Fetch weather (will use cache if available)
result = get_weather("london")
print(result)
# Output: ('london', 290.5, 65, 'clear sky', '22/12/2025, 14:30:00')
```

## Testing

**5 comprehensive tests:**

1. ✅ `test_get_weather_no_cache` - Fetch from API when cache empty
2. ✅ `test_get_weather_from_cache` - Read from fresh cache (< 1 min)
3. ✅ `test_connection_error` - Retry 3 times on network failure
4. ✅ `test_old_cache` - Refresh stale cache (> 1 min)
5. ✅ `test_invalid_city` - Handle invalid city input

**All tests use mocking:**
- No real API calls during testing
- No real database writes
- Fast and isolated tests

## What I Learned

### New Concepts (Day 58):
- ✅ `unittest.mock` - Mocking external dependencies
- ✅ `patch()` - Replacing functions with fakes
- ✅ `side_effect` - Simulating exceptions
- ✅ `assert_called_once()` / `assert_not_called()` - Verifying behavior
- ✅ Testing retry logic with mocks
- ✅ Mocking API responses without hitting real endpoints

### Skills Reinforced:
- Decorators (retry pattern)
- SQLite caching strategies
- Error handling patterns
- datetime calculations
- Test-driven development

## API Response Format

OpenWeatherMap returns:
```json
{
  "main": {
    "temp": 290.5,
    "humidity": 65
  },
  "weather": [
    {"description": "clear sky"}
  ]
}
```

## Future Improvements

- [ ] Add more cities
- [ ] Make cache TTL configurable
- [ ] Add temperature unit conversion (Kelvin → Celsius)
- [ ] Environment variables for API key
- [ ] Rate limiting
- [ ] Command-line interface

## Project Stats

- **Time Spent:** 4 hours
- **Lines of Code:** ~120 (excluding tests)
- **Tests:** 5 (all passing ✅)
- **From Memory:** ~75% (mocking was new)

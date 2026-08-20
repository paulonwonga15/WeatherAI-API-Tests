from utils.api_client import WeatherAIClient
import pytest
import time
def test_get_weather_success():
    client = WeatherAIClient()
    response = client.get_weather(
        lat=-1.2921,
        lon=36.8219,
        units="metric",
        days=7
    )
    # 1. HTTP status
    assert response.status_code == 200
    # 2. Response must be JSON
    data = response.json()
    assert isinstance(data, dict)
    # 3. Required top-level fields
    assert "lat" in data
    assert "lon" in data
    assert "current" in data
    assert "daily" in data
    assert "hourly" in data
    # 4. Location should match the request
    assert data["lat"] == -1.2921
    assert data["lon"] == 36.8219
    # 5. Current weather should contain important fields
    current = data["current"]
    assert "time" in current
    assert "temperature" in current
    assert "windspeed" in current
    assert "weathercode" in current
    # 6. Temperature should be numeric
    assert isinstance(current["temperature"], (int, float))
    # 7. Daily forecast should contain 7 days
    assert isinstance(data["daily"], list)
    assert len(data["daily"]) == 7
    # 8. Each daily forecast should contain required fields
    for day in data["daily"]:
        assert "date" in day
        assert "temp_max" in day
        assert "temp_min" in day
        assert "weathercode" in day
def test_invalid_latitude():
    client = WeatherAIClient()

    response = client.get_weather(
        lat=200,
        lon=36.8219,
        units="metric",
        days=7
    )

    # WeatherAI currently returns 502 for an out-of-range latitude.
    assert response.status_code == 502


def test_invalid_longitude():
    client = WeatherAIClient()

    response = client.get_weather(
        lat=-1.2921,
        lon=250,
        units="metric",
        days=7
    )

    # WeatherAI currently returns 502 for an out-of-range longitude.
    assert response.status_code == 502
def test_invalid_api_key():
    client = WeatherAIClient()

    # Replace the valid key in memory with a deliberately invalid key.
    client.headers["Authorization"] = "Bearer wai_invalid_test_key"

    response = client.get_weather(
        lat=-1.2921,
        lon=36.8219,
        units="metric",
        days=7
    )

    assert response.status_code == 401, (
        f"Expected 401 Unauthorized for invalid API key, "
        f"but received {response.status_code}: {response.text}"
    )
def test_missing_latitude():
    client = WeatherAIClient()

    response = client.get_weather(
        lon=36.8219,
        units="metric",
        days=7
    )

    assert response.status_code == 400, (
        f"Expected 400 Bad Request when latitude is missing, "
        f"but received {response.status_code}: {response.text}"
    )


def test_missing_longitude():
    client = WeatherAIClient()

    response = client.get_weather(
        lat=-1.2921,
        units="metric",
        days=7
    )

    assert response.status_code == 400, (
        f"Expected 400 Bad Request when longitude is missing, "
        f"but received {response.status_code}: {response.text}"
    )
def test_weather_data_quality():
    client = WeatherAIClient()

    response = client.get_weather(
        lat=-1.2921,
        lon=36.8219,
        units="metric",
        days=7
    )

    assert response.status_code == 200

    data = response.json()

    # Validate current weather
    current = data["current"]

    assert isinstance(current["temperature"], (int, float))
    assert isinstance(current["windspeed"], (int, float))
    assert current["windspeed"] >= 0

    # Validate daily forecast data
    for day in data["daily"]:
        assert day["temp_max"] >= day["temp_min"]
        assert isinstance(day["precipitation"], (int, float))
        assert day["precipitation"] >= 0
        assert isinstance(day["weathercode"], int)
@pytest.mark.parametrize(
    "city, lat, lon",
    [
        ("Nairobi", -1.2921, 36.8219),
        ("Kisumu", -0.0917, 34.7680),
        ("Mombasa", -4.0435, 39.6682),
    ]
)
def test_weather_multiple_locations(city, lat, lon):
    client = WeatherAIClient()

    response = client.get_weather(
        lat=lat,
        lon=lon,
        units="metric",
        days=7
    )

    assert response.status_code == 200

    data = response.json()

    assert "current" in data
    assert "daily" in data

    assert isinstance(data["current"]["temperature"], (int, float))
    assert len(data["daily"]) == 7
def test_weather_response_time():
    client = WeatherAIClient()

    start_time = time.perf_counter()

    response = client.get_weather(
        lat=-1.2921,
        lon=36.8219,
        units="metric",
        days=7
    )

    response_time = time.perf_counter() - start_time

    assert response.status_code == 200
    assert response_time < 5, (
        f"API response took {response_time:.2f} seconds, "
        f"which exceeds the 5-second threshold"
    )

    print(f"\nAPI response time: {response_time:.2f} seconds")
from utils.api_client import WeatherAIClient
import pytest
import time


# ============================================================
# CORE WEATHER API / SUCCESS CASES
# ============================================================

def test_get_weather_success():
    client = WeatherAIClient()

    response = client.get_weather(
        lat=-1.2921,
        lon=36.8219,
        units="metric",
        days=7
    )

    # HTTP status
    assert response.status_code == 200

    # Response must be JSON
    data = response.json()
    assert isinstance(data, dict)

    # Required top-level fields
    assert "lat" in data
    assert "lon" in data
    assert "current" in data
    assert "daily" in data
    assert "hourly" in data

    # Location should match the request
    assert data["lat"] == -1.2921
    assert data["lon"] == 36.8219

    # Current weather required fields
    current = data["current"]

    assert "time" in current
    assert "temperature" in current
    assert "windspeed" in current
    assert "weathercode" in current

    # Temperature should be numeric
    assert isinstance(current["temperature"], (int, float))

    # Daily forecast should contain 7 days
    assert isinstance(data["daily"], list)
    assert len(data["daily"]) == 7

    # Validate required daily forecast fields
    for day in data["daily"]:
        assert "date" in day
        assert "temp_max" in day
        assert "temp_min" in day
        assert "weathercode" in day


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

# ============================================================
# PERFORMANCE TESTING
# Verifies API response time for a standard weather request.
# ============================================================
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


# ============================================================
# AUTHENTICATION
# ============================================================

def test_invalid_api_key():
    client = WeatherAIClient()

    # Replace valid API key with deliberately invalid key
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


# ============================================================
# LATITUDE AND LONGITUDE VALIDATION
# ============================================================

def test_invalid_latitude():
    client = WeatherAIClient()

    response = client.get_weather(
        lat=200,
        lon=36.8219,
        units="metric",
        days=7
    )

    # WeatherAI currently returns 502 for out-of-range latitude
    assert response.status_code == 502


def test_invalid_longitude():
    client = WeatherAIClient()

    response = client.get_weather(
        lat=-1.2921,
        lon=250,
        units="metric",
        days=7
    )

    # WeatherAI currently returns 502 for out-of-range longitude
    assert response.status_code == 502


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


def test_invalid_latitude_type():
    client = WeatherAIClient()

    response = client.get_weather(
        lat="abc",
        lon=36.8219,
        units="metric",
        days=7
    )

    assert response.status_code >= 400


def test_invalid_longitude_type():
    client = WeatherAIClient()

    response = client.get_weather(
        lat=-1.2921,
        lon="abc",
        units="metric",
        days=7
    )

    assert response.status_code >= 400


def test_empty_latitude_is_handled():
    client = WeatherAIClient()

    response = client.get_weather(
        lat="",
        lon=36.8219,
        units="metric",
        days=7
    )

    # Current API behavior: empty latitude is accepted
    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, dict)
    assert "current" in data
    assert "daily" in data


def test_empty_longitude_is_handled():
    client = WeatherAIClient()

    response = client.get_weather(
        lat=-1.2921,
        lon="",
        units="metric",
        days=7
    )

    # Current API behavior: empty longitude is accepted
    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, dict)
    assert "current" in data
    assert "daily" in data


def test_latitude_upper_boundary():
    client = WeatherAIClient()

    response = client.get_weather(
        lat=90,
        lon=36.8219,
        units="metric",
        days=7
    )

    assert response.status_code == 200


def test_latitude_lower_boundary():
    client = WeatherAIClient()

    response = client.get_weather(
        lat=-90,
        lon=36.8219,
        units="metric",
        days=7
    )

    assert response.status_code == 200


def test_longitude_upper_boundary():
    client = WeatherAIClient()

    response = client.get_weather(
        lat=-1.2921,
        lon=180,
        units="metric",
        days=7
    )

    assert response.status_code == 200


def test_longitude_lower_boundary():
    client = WeatherAIClient()

    response = client.get_weather(
        lat=-1.2921,
        lon=-180,
        units="metric",
        days=7
    )

    assert response.status_code == 200


def test_zero_coordinates():
    client = WeatherAIClient()

    response = client.get_weather(
        lat=0,
        lon=0,
        units="metric",
        days=7
    )

    assert response.status_code == 200


def test_very_large_coordinates():
    client = WeatherAIClient()

    response = client.get_weather(
        lat=999999,
        lon=999999,
        units="metric",
        days=7
    )

    assert response.status_code >= 400

    print(
        f"\nVery large coordinates response: "
        f"{response.status_code}"
    )


def test_boolean_coordinates():
    client = WeatherAIClient()

    response = client.get_weather(
        lat=True,
        lon=False,
        units="metric",
        days=7
    )

    # Python treats booleans as integers.
    # This verifies the API rejects boolean coordinates.
    assert response.status_code >= 400

    print(
        f"\nBoolean coordinates response: "
        f"{response.status_code}"
    )


# ============================================================
# FORECAST DAYS VALIDATION
# ============================================================

def test_weather_default_parameters():
    client = WeatherAIClient()

    response = client.get_weather(
        lat=-1.2921,
        lon=36.8219
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, dict)
    assert "current" in data
    assert "daily" in data
    assert len(data["daily"]) == 7


def test_weather_one_day_forecast():
    client = WeatherAIClient()

    response = client.get_weather(
        lat=-1.2921,
        lon=36.8219,
        units="metric",
        days=1
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data["daily"], list)
    assert len(data["daily"]) == 1


def test_weather_seven_day_forecast():
    client = WeatherAIClient()

    response = client.get_weather(
        lat=-1.2921,
        lon=36.8219,
        units="metric",
        days=7
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data["daily"], list)
    assert len(data["daily"]) == 7


def test_days_zero_is_normalized():
    client = WeatherAIClient()

    response = client.get_weather(
        lat=-1.2921,
        lon=36.8219,
        units="metric",
        days=0
    )

    assert response.status_code == 200

    data = response.json()

    assert data["days"] == 7
    assert len(data["daily"]) == 7


def test_days_above_maximum_is_normalized():
    client = WeatherAIClient()

    response = client.get_weather(
        lat=-1.2921,
        lon=36.8219,
        units="metric",
        days=8
    )

    assert response.status_code == 200

    data = response.json()

    assert data["days"] == 7
    assert len(data["daily"]) == 7


def test_negative_days():
    client = WeatherAIClient()

    response = client.get_weather(
        lat=-1.2921,
        lon=36.8219,
        units="metric",
        days=-1
    )

    assert response.status_code == 200

    data = response.json()

    print("\nNegative days normalized to:", data.get("days"))

    assert isinstance(data["days"], int)
    assert data["days"] >= 1


def test_invalid_days_type():
    client = WeatherAIClient()

    response = client.get_weather(
        lat=-1.2921,
        lon=36.8219,
        units="metric",
        days="abc"
    )

    print(
        "Invalid days normalized to:",
        response.json().get("days")
    )

    assert response.status_code == 200


def test_empty_days():
    client = WeatherAIClient()

    response = client.get_weather(
        lat=-1.2921,
        lon=36.8219,
        units="metric",
        days=""
    )

    print(
        "Empty days normalized to:",
        response.json().get("days")
    )

    assert response.status_code == 200


def test_decimal_days():
    client = WeatherAIClient()

    response = client.get_weather(
        lat=-1.2921,
        lon=36.8219,
        units="metric",
        days=3.5
    )

    # WeatherAI currently returns 502 for decimal days
    assert response.status_code == 502, (
        f"Expected 502 for decimal days, "
        f"but received {response.status_code}: {response.text}"
    )


# ============================================================
# UNITS VALIDATION
# ============================================================

def test_weather_imperial_units():
    client = WeatherAIClient()

    response = client.get_weather(
        lat=-1.2921,
        lon=36.8219,
        units="imperial",
        days=7
    )

    assert response.status_code == 200

    data = response.json()

    assert "current" in data
    assert isinstance(data["current"]["temperature"], (int, float))


def test_invalid_units_value():
    client = WeatherAIClient()

    response = client.get_weather(
        lat=-1.2921,
        lon=36.8219,
        units="invalid",
        days=7
    )

    assert response.status_code == 200

    data = response.json()

    print("\nInvalid units response:", data.get("units"))

    # Current API behavior: invalid value is normalized
    assert data["units"] in ["metric", "imperial"]


def test_empty_units():
    client = WeatherAIClient()

    response = client.get_weather(
        lat=-1.2921,
        lon=36.8219,
        units="",
        days=7
    )

    assert response.status_code == 200

    data = response.json()

    print("\nEmpty units normalized to:", data.get("units"))

    # Current API behavior: empty value is normalized
    assert data["units"] in ["metric", "imperial"]


@pytest.mark.parametrize("units", ["METRIC", "Metric"])
def test_units_case_sensitivity(units):
    client = WeatherAIClient()

    response = client.get_weather(
        lat=-1.2921,
        lon=36.8219,
        units=units,
        days=7
    )

    assert response.status_code == 200

    data = response.json()

    print(f"\nUnits '{units}' returned:", data.get("units"))

    # Current API behavior: case variation is accepted/normalized
    assert data["units"] in ["metric", "imperial"]


# ============================================================
# OPTIONAL PARAMETERS / API CONTRACT
# ============================================================

def test_weather_ai_disabled():
    client = WeatherAIClient()

    response = client.get_weather(
        lat=-1.2921,
        lon=36.8219,
        units="metric",
        days=7,
        ai="false"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, dict)
    assert "current" in data
    assert "daily" in data


def test_extra_unknown_parameter():
    client = WeatherAIClient()

    response = client.get_weather(
        lat=-1.2921,
        lon=36.8219,
        units="metric",
        days=7,
        foo="bar"
    )

    assert response.status_code == 200

    data = response.json()

    assert "current" in data
    assert "daily" in data
    assert "hourly" in data

    print("\nExtra parameter accepted successfully")


# ============================================================
# RESPONSE FORMAT
# ============================================================

def test_weather_response_is_json():
    client = WeatherAIClient()

    response = client.get_weather(
        lat=-1.2921,
        lon=36.8219,
        units="metric",
        days=7
    )

    assert response.status_code == 200

    content_type = response.headers.get("Content-Type", "").lower()

    assert "application/json" in content_type

    data = response.json()

    assert isinstance(data, dict)


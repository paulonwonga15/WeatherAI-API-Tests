from utils.api_client import WeatherAIClient
import pytest
import time


# ============================================================
# TEST OUTPUT HELPER
# ============================================================

def print_response(label, response):
    print(f"\n{'=' * 60}")
    print(label)
    print(f"Status code: {response.status_code}")

    try:
        print(f"Response: {response.json()}")
    except ValueError:
        print(f"Response: {response.text}")

    print(f"{'=' * 60}")


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

    print_response("Successful weather request - Nairobi", response)

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, dict)

    assert "lat" in data
    assert "lon" in data
    assert "current" in data
    assert "daily" in data
    assert "hourly" in data

    assert data["lat"] == -1.2921
    assert data["lon"] == 36.8219

    current = data["current"]

    assert "time" in current
    assert "temperature" in current
    assert "windspeed" in current
    assert "weathercode" in current

    assert isinstance(current["temperature"], (int, float))

    assert isinstance(data["daily"], list)
    assert len(data["daily"]) == 7

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

    print_response("Weather data quality - Nairobi", response)

    assert response.status_code == 200

    data = response.json()

    current = data["current"]

    assert isinstance(current["temperature"], (int, float))
    assert isinstance(current["windspeed"], (int, float))
    assert current["windspeed"] >= 0

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

    print_response(f"Multiple location test - {city}", response)

    assert response.status_code == 200

    data = response.json()

    assert "current" in data
    assert "daily" in data

    assert isinstance(data["current"]["temperature"], (int, float))
    assert len(data["daily"]) == 7


# ============================================================
# PERFORMANCE TESTING
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

    print_response("API response time test", response)
    print(f"API response time: {response_time:.2f} seconds")

    assert response.status_code == 200

    assert response_time < 5, (
        f"API response took {response_time:.2f} seconds, "
        f"which exceeds the 5-second threshold"
    )


# ============================================================
# AUTHENTICATION
# ============================================================

def test_invalid_api_key():
    client = WeatherAIClient()

    client.headers["Authorization"] = "Bearer wai_invalid_test_key"

    response = client.get_weather(
        lat=-1.2921,
        lon=36.8219,
        units="metric",
        days=7
    )

    print_response("Invalid API key authentication test", response)

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

    print_response("Invalid latitude - lat=200", response)

    # Observed WeatherAI behavior: 502
    assert response.status_code == 502


def test_invalid_longitude():
    client = WeatherAIClient()

    response = client.get_weather(
        lat=-1.2921,
        lon=250,
        units="metric",
        days=7
    )

    print_response("Invalid longitude - lon=250", response)

    # Observed WeatherAI behavior: 502
    assert response.status_code == 502


def test_missing_latitude():
    client = WeatherAIClient()

    response = client.get_weather(
        lon=36.8219,
        units="metric",
        days=7
    )

    print_response("Missing latitude", response)

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

    print_response("Missing longitude", response)

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

    print_response("Invalid latitude type - lat='abc'", response)

    assert response.status_code == 400


def test_invalid_longitude_type():
    client = WeatherAIClient()

    response = client.get_weather(
        lat=-1.2921,
        lon="abc",
        units="metric",
        days=7
    )

    print_response("Invalid longitude type - lon='abc'", response)

    assert response.status_code == 400


def test_empty_latitude_is_handled():
    client = WeatherAIClient()

    response = client.get_weather(
        lat="",
        lon=36.8219,
        units="metric",
        days=7
    )

    print_response("Empty latitude - lat=''", response)

    # Observed API behavior: accepted
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

    print_response("Empty longitude - lon=''", response)

    # Observed API behavior: accepted
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

    print_response("Latitude upper boundary - lat=90", response)

    assert response.status_code == 200


def test_latitude_lower_boundary():
    client = WeatherAIClient()

    response = client.get_weather(
        lat=-90,
        lon=36.8219,
        units="metric",
        days=7
    )

    print_response("Latitude lower boundary - lat=-90", response)

    assert response.status_code == 200


def test_longitude_upper_boundary():
    client = WeatherAIClient()

    response = client.get_weather(
        lat=-1.2921,
        lon=180,
        units="metric",
        days=7
    )

    print_response("Longitude upper boundary - lon=180", response)

    assert response.status_code == 200


def test_longitude_lower_boundary():
    client = WeatherAIClient()

    response = client.get_weather(
        lat=-1.2921,
        lon=-180,
        units="metric",
        days=7
    )

    print_response("Longitude lower boundary - lon=-180", response)

    assert response.status_code == 200


def test_zero_coordinates():
    client = WeatherAIClient()

    response = client.get_weather(
        lat=0,
        lon=0,
        units="metric",
        days=7
    )

    print_response("Zero coordinates - lat=0, lon=0", response)

    assert response.status_code == 200


def test_very_large_coordinates():
    client = WeatherAIClient()

    response = client.get_weather(
        lat=999999,
        lon=999999,
        units="metric",
        days=7
    )

    print_response(
        "Very large coordinates - lat=999999, lon=999999",
        response
    )

    # Observed API behavior: 502 Bad gateway
    assert response.status_code == 502


def test_boolean_coordinates():
    client = WeatherAIClient()

    response = client.get_weather(
        lat=True,
        lon=False,
        units="metric",
        days=7
    )

    print_response(
        "Boolean coordinates - lat=True, lon=False",
        response
    )

    assert response.status_code >= 400


# ============================================================
# FORECAST DAYS VALIDATION
# ============================================================

def test_weather_default_parameters():
    client = WeatherAIClient()

    response = client.get_weather(
        lat=-1.2921,
        lon=36.8219
    )

    print_response("Default forecast parameters", response)

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

    print_response("One-day forecast - days=1", response)

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

    print_response("Seven-day forecast - days=7", response)

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

    print_response("Zero forecast days - days=0", response)

    assert response.status_code == 200

    data = response.json()

    print(f"Normalized days value: {data.get('days')}")

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

    print_response("Days above maximum - days=8", response)

    assert response.status_code == 200

    data = response.json()

    print(f"Normalized days value: {data.get('days')}")

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

    print_response("Negative forecast days - days=-1", response)

    assert response.status_code == 200

    data = response.json()

    print(f"Normalized days value: {data.get('days')}")

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

    print_response("Invalid days type - days='abc'", response)

    data = response.json()

    print(f"Normalized days value: {data.get('days')}")

    assert response.status_code == 200


def test_empty_days():
    client = WeatherAIClient()

    response = client.get_weather(
        lat=-1.2921,
        lon=36.8219,
        units="metric",
        days=""
    )

    print_response("Empty days - days=''", response)

    data = response.json()

    print(f"Normalized days value: {data.get('days')}")

    assert response.status_code == 200


def test_decimal_days():
    client = WeatherAIClient()

    response = client.get_weather(
        lat=-1.2921,
        lon=36.8219,
        units="metric",
        days=3.5
    )

    print_response("Decimal forecast days - days=3.5", response)

    # Observed WeatherAI behavior: 502
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

    print_response("Imperial units", response)

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

    print_response("Invalid units - units='invalid'", response)

    assert response.status_code == 200

    data = response.json()

    print(f"Normalized units value: {data.get('units')}")

    assert data["units"] in ["metric", "imperial"]


def test_empty_units():
    client = WeatherAIClient()

    response = client.get_weather(
        lat=-1.2921,
        lon=36.8219,
        units="",
        days=7
    )

    print_response("Empty units - units=''", response)

    assert response.status_code == 200

    data = response.json()

    print(f"Normalized units value: {data.get('units')}")

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

    print_response(
        f"Units case variation - units='{units}'",
        response
    )

    assert response.status_code == 200

    data = response.json()

    print(f"Normalized units value: {data.get('units')}")

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

    print_response("AI disabled - ai='false'", response)

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

    print_response("Unknown parameter - foo='bar'", response)

    assert response.status_code == 200

    data = response.json()

    assert "current" in data
    assert "daily" in data
    assert "hourly" in data

    print("Extra parameter accepted successfully")


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

    print_response("JSON response validation", response)

    assert response.status_code == 200

    content_type = response.headers.get("Content-Type", "").lower()

    print(f"Content-Type: {content_type}")

    assert "application/json" in content_type

    data = response.json()

    assert isinstance(data, dict)
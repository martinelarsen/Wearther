import streamlit as st
import requests
from datetime import datetime, timedelta, timezone
import pytz
from timezonefinder import TimezoneFinder
import pandas as pd

@st.cache_data(ttl=300)
def geocode_city(city_query: str):
    """Geocode city to lat/lon/display name."""
    if not city_query.strip():
        return None
    url = f"https://nominatim.openstreetmap.org/search?q={city_query}&format=json&limit=1"
    headers = {'User-Agent': 'WeartherApp'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        result = response.json()
        top = result[0]
        return round(float(top['lat']), 4), round(float(top['lon']), 4), top.get('display_name', city_query) # MET Norway API do not like too precise coords
    except Exception as e:
        st.error(f"Nominatim API error: {e}")
        return None

@st.cache_data(ttl=1800)  # 30 min
def get_forecast_df(lat: float, lon: float) -> pd.DataFrame:
    """Fetch and process 7-day forecast (hourly) with local times."""
    url = f"https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={lat}&lon={lon}"
    headers = {'User-Agent': 'WeartherApp'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        timeseries = response.json()['properties']['timeseries']
    except Exception as e:
        st.error(f"MET Norway API error: {e}")
        return pd.DataFrame()

    now_utc = datetime.now(timezone.utc)
    end_time = now_utc.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=8)

    forecast_list = []
    tf = TimezoneFinder()
    tz_name = tf.timezone_at(lat=lat, lng=lon)
    local_tz = pytz.timezone(tz_name) if tz_name else pytz.UTC

    for entry in timeseries:
        timestamp_str = entry['time'].replace('Z', '+00:00')
        timestamp_utc = datetime.fromisoformat(timestamp_str)
        if now_utc <= timestamp_utc < end_time:
            instant = entry['data']['instant']['details']
            next_1h = entry['data'].get('next_1_hours', {})
            forecast_list.append({
                'datetime_utc': timestamp_utc,
                'temperature': instant.get('air_temperature'),
                'precipitation_mm': next_1h.get('details', {}).get('precipitation_amount', 0),
                'symbol_code': next_1h.get('summary', {}).get('symbol_code', 'unknown'), 
                'wind_speed_mps': instant.get('wind_speed', 0)
            })
    
    df = pd.DataFrame(forecast_list)
    df['datetime_utc'] = pd.to_datetime(df['datetime_utc'], utc=True)
    df = df.set_index('datetime_utc')

    today_local = datetime.now(local_tz).replace(hour=0, minute=0, second=0, microsecond=0)
    last_local_day = today_local + timedelta(days=7)
    end_local = last_local_day.replace(hour=23)
    end_utc = end_local.astimezone(pytz.UTC)

    # Build full hourly index
    full_index = pd.date_range(
        start=df.index[0],
        end=end_utc,
        freq='1h'
    )

    df = df.reindex(full_index).ffill()
    df = df.reset_index().rename(columns={'index': 'datetime_utc'})

    df['datetime_local'] = df['datetime_utc'].dt.tz_convert(local_tz)
    df['local_date'] = df['datetime_local'].dt.strftime('%Y-%m-%d')
    df['day_name'] = df['datetime_local'].dt.day_name()
    df['date_display'] = df['datetime_local'].dt.strftime('%B %d')
    df['local_time_short'] = df['datetime_local'].dt.strftime('%H:%M')

    today_local = datetime.now(local_tz).replace(hour=0, minute=0, second=0, microsecond=0)
    df['day_offset'] = (df['datetime_local'].dt.normalize() - today_local).dt.days.astype(int)

    return df

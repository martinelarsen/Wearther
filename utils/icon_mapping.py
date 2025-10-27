from utils.config import PRECIP_LIGHT, PRECIP_MODERATE, WIND_MODERATE, WIND_STRONG, SNOW_VARIANTS, SUNNY_VARIANTS, TEMP_CLOTHING_RULES, CATEGORY_ORDER
from utils.weather_api import get_forecast_df
import pandas as pd
import streamlit as st

def get_icons_for_conditions(row):
    """Map weather row to icons: temp -> precip -> wind -> lightning -> sun."""
    temp = row.get('temperature')
    precip_mm = row.get('precipitation_mm')
    wind = row.get('wind_speed_mps')
    symbol_code = row.get('symbol_code')

    categories = {cat: [] for cat in CATEGORY_ORDER}

    # Step 1: Temperature-based clothing
    for threshold, icons in TEMP_CLOTHING_RULES:
        if temp < threshold:
            for cat, icon_list in icons.items():
                for icon in icon_list:
                    categories[cat].append(icon)
            break

    # Step 2: precipitation
    if precip_mm > 0:
        is_snow = any(variant in symbol_code for variant in SNOW_VARIANTS)
        if is_snow:
            categories['precipitation'].append('snowman' if 'heavysnow' in symbol_code else 'snowflake')
        else:
            # Rain intensity
            if precip_mm > PRECIP_MODERATE:
                categories['precipitation'].append('umbrella-with-rain-drops')
                categories['precipitation'].append('rain-boots')
                categories['precipitation'].append('rain-coat')
            elif precip_mm > PRECIP_LIGHT:
                categories['precipitation'].append('umbrella-with-rain-drops')
            else:
                categories['precipitation'].append('umbrella')

    # Step 3: wind 
    if wind > WIND_MODERATE:
        if wind > WIND_STRONG:
            categories['wind'].append('wind-face')
            categories['wind'].append('kite')
        else:
            categories['wind'].append('wind-face')

    # Step 4: lightning/thunder 
    if 'thunder' in symbol_code:
        categories['lightning'].append('lightning')

    # Step 5: Sun
    if any(variant in symbol_code for variant in SUNNY_VARIANTS) and precip_mm <= 0:
        categories['accessories'].append('sunglasses')
        if temp is not None and temp >= 20:
            categories['accessories'].append('sun-cream')

    # Step 6: Modify precipitation based on wind/lightning
    if wind > WIND_MODERATE or 'thunder' in symbol_code:
        if precip_mm > 0: # Disable umbrellas
            umbrellas = ['umbrella', 'umbrella-with-rain-drops']
            categories['precipitation'] = [i for i in categories['precipitation'] if i not in umbrellas]
            categories['precipitation'].append('umbrella-cross')
            if not is_snow: # add raincoat (if not snow)
                if 'rain-coat' not in categories['precipitation']:
                    categories['precipitation'].append('rain-coat')

    return categories

def add_icons_to_weather_data(lat, lon):
    """Fetch forecast and add categories to each row."""
    df = get_forecast_df(lat, lon)
    if df is None or df.empty:
        return pd.DataFrame()
    df['categories'] = df.apply(get_icons_for_conditions, axis=1)
    return df.sort_values('datetime_local')

def group_similar_hours(df):
    """Group consecutive hours with identical icons."""
    if df.empty:
        return []
    
    df = df.copy()

    def cat_key(cats):
        return tuple(sorted((k, tuple(sorted(v))) for k, v in cats.items()))

    df['cat_key'] = df['categories'].apply(cat_key)
    groups, current = [], [0]
    for i in range(1, len(df)):
        if df.iloc[i]['cat_key'] == df.iloc[i-1]['cat_key']:
            current.append(i)
        else:
            groups.append(current)
            current = [i]
    groups.append(current)
    return groups

def get_ordered_icons(categories):
    """Order icons by category sequence with spacers."""
    ordered = []
    for cat in CATEGORY_ORDER:
        cat_icons = categories.get(cat, [])
        ordered.extend(cat_icons) 

        # Add spacers between certain categories
        if cat == 'coats' and categories.get('accessories'):
            ordered.append('spacer')
        elif cat == 'accessories' and (categories.get('precipitation') or categories.get('wind')):
            ordered.append('spacer')
        elif cat == 'precipitation' and categories.get('wind'):
            ordered.append('spacer')

    return ordered

import streamlit as st
from datetime import datetime, timedelta
from utils.config import ICON_CATEGORIES
import os
from utils.display_helpers import display_today_forecast, get_icons_from_df
from utils.ui_helpers import render_if_location_set, render_icon_help, render_footer, setup_sidebar_location

setup_sidebar_location()

st.title("🕒 Wearther: Until Home")

def display_today(df):
    filtered_df =  display_today_forecast(df, with_selectbox=True)

    if filtered_df is not None:
        render_icon_help(filtered_df)

render_if_location_set(display_today)          
render_footer()

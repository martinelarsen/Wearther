import streamlit as st
from utils.display_helpers import display_hourly_forecast, render_day_expanders, render_expand_button
from utils.ui_helpers import setup_sidebar_location, render_if_location_set, render_footer

setup_sidebar_location()

st.title("🔮 Wearther: Long Term Forecast")

def display_long_term(df):
    render_expand_button()
    render_day_expanders(df, display_hourly_forecast)

render_if_location_set(display_long_term)
render_footer()
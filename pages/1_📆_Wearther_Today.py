import streamlit as st
from utils.display_helpers import display_today_forecast
from utils.ui_helpers import setup_sidebar_location, render_if_location_set, render_footer

setup_sidebar_location()

st.title("📆 Wearther: Today")

def display_today(df):
    display_today_forecast(df, with_selectbox=False)

render_if_location_set(display_today)
render_footer()

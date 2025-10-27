import streamlit as st
from utils.display_helpers import display_daily_packing, render_day_expanders, render_expand_button
from utils.ui_helpers import setup_sidebar_location, render_if_location_set, render_footer

setup_sidebar_location()

st.title("🧳 Wearther: Packing List")

def display_packing(df):
    render_expand_button()
    render_day_expanders(df, display_daily_packing)

render_if_location_set(display_packing)
render_footer()
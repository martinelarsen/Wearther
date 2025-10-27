import streamlit as st
from datetime import datetime, timedelta
from utils.config import ICON_CATEGORIES
import os
from utils.display_helpers import display_icon_legend, display_today_forecast, get_icons_from_today
from utils.ui_helpers import render_if_location_set, render_footer, setup_sidebar_location

setup_sidebar_location()

def display_today(df):
    display_today_forecast(df, with_selectbox=True)

    icons_present = get_icons_from_today(df)

    with st.expander("What do these icons mean?"):
        display_icon_legend(icons_present, icon_size=30)

render_if_location_set(display_today)          
render_footer()

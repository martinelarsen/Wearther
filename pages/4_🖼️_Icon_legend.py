import streamlit as st
import os
from utils.display_helpers import display_icon_legend
from utils.ui_helpers import setup_sidebar_location, render_footer
from utils.config import ICON_CATEGORIES

setup_sidebar_location()

st.title("🖼️ Icon Legend")
st.write("All icons used in Wearther are from [SVGrepo.com](https://www.svgrepo.com/) and are categorized as follows:")

display_icon_legend()

render_footer()
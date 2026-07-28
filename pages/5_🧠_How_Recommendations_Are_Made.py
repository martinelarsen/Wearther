import streamlit as st

from utils.ui_helpers import setup_sidebar_location, render_footer
from utils.display_helpers import display_icons
from utils.config import TEMP_CLOTHING_RULES


setup_sidebar_location()


st.title("🧠 How Recommendations Are Made")

st.write(
"""
Wearther converts hourly weather forecasts into practical clothing
recommendations using a rule-based decision engine.

The recommendation process has three steps:
"""
)

overview_cols = st.columns(3)

steps = [
    (
        "🌡️ 1. Base outfit",
        "Temperature selects the starting outfit."
    ),
    (
        "🌧️ 2. Weather modifiers",
        "Weather conditions adjust the recommendation."
    ),
    (
        "🕒 3. Grouping",
        "Identical recommendations are grouped together."
    ),
]

for col, (title, description) in zip(overview_cols, steps):
    with col:
        with st.container(border=True):
            st.subheader(title)
            st.caption(description)

st.divider()

# -------------------------------------------------
# Temperature
# -------------------------------------------------

st.header("1. Temperature determines the base outfit")

st.write(
"""
Temperature selects the starting outfit. Weather conditions such as rain,
wind, and thunderstorms then modify this recommendation.
"""
)


def format_temperature_range(index, rules):
    threshold = rules[index][0]

    if index == 0:
        return f"< {threshold}°C"
    elif threshold == 100:
        return "> 25°C"
    else:
        previous = rules[index - 1][0]
        return f"{previous}°C to {threshold}°C"


temperature_cols = st.columns(2)

for i, (_, icons) in enumerate(TEMP_CLOTHING_RULES):

    with temperature_cols[i % 2]:
        with st.container(border=True):

            st.subheader(format_temperature_range(i, TEMP_CLOTHING_RULES))

            categories = {
                "tops": icons.get("tops", []),
                "bottoms": icons.get("bottoms", []),
                "coats": icons.get("coats", []),
                "accessories": icons.get("accessories", []),
                "precipitation": [],
                "wind": [],
                "lightning": []
            }

            display_icons(categories, add_spacers=False)

# -------------------------------------------------
# Weather modifiers
# -------------------------------------------------

st.header("2. Weather conditions modify the outfit")

st.write(
"""
Weather conditions add protection or override unsuitable choices.
"""
)


modifiers = [
    (
        "🌧️ Rain",
        "Light rain shows an umbrella. Heavier rain adds more protection.",
        {
            "precipitation": [
                "umbrella",
                "umbrella-with-rain-drops",
                "rain-boots",
                "rain-coat"
            ]
        }
    ),

    (
        "🌬️ Strong wind",
        "Displays wind conditions and warnings",
        {
            "wind": [
                "wind-face",
                "kite"
            ]
        }
    ),

    (
        "⛈️ Thunderstorm",
        "Umbrellas are replaced with safer rain protection",
        {
            "coats": ["rain-coat"],
            "precipitation": ["umbrella-cross"],
            "lightning": ["lightning"]
        }
    ),

    (
        "☀️ Sunny weather",
        "Adds sun protection",
        {
            "accessories": [
                "sunglasses",
                "sun-cream"
            ]
        }
    )
]


modifier_cols = st.columns(2)

for i, (title, description, icons) in enumerate(modifiers):

    with modifier_cols[i % 2]:

        with st.container(border=True):

            st.subheader(title)
            st.caption(description)

            categories = {
                "tops": [],
                "bottoms": [],
                "coats": icons.get("coats", []),
                "accessories": icons.get("accessories", []),
                "precipitation": icons.get("precipitation", []),
                "wind": icons.get("wind", []),
                "lightning": icons.get("lightning", [])
            }

            display_icons(categories, add_spacers=False)
   
# -------------------------------------------------
# Grouping
# -------------------------------------------------

st.header("3. Grouping similar recommendations")

st.write(
"""
Hourly forecasts with identical recommendations are grouped together.
This reduces repetition and makes the forecast easier to understand.
"""
)


col1, col2 = st.columns(2)


with col1:
    st.caption("Without grouping")

    st.code(
"""
08:00  👕 👖 ☔️
09:00  👕 👖 ☔️
10:00  👕 👖 ☔️
11:00  👕 👖 ☔️
"""
)


with col2:
    st.caption("With grouping")

    st.code(
"""
08:00-12:00 👕 👖 ☔️
"""
)


st.divider()


st.info(
"""
Wearther uses explicit rules instead of machine learning. This makes the
recommendations transparent, predictable and easy to adjust.
"""
)


render_footer()
import streamlit as st
from utils.weather_api import geocode_city
from utils.icon_mapping import add_icons_to_weather_data
from utils.display_helpers import display_icon_legend, get_icons_from_df

def init_session_state():
    """Initialize session state defaults if not set."""
    defaults = {
        'current_location': None,
        'current_coords': None,
        'show_search': True,
        'weather_df': None,
        'expand_all': False
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)

def reset_location():
    """Reset location-related session state."""
    for key in ['current_location', 'current_coords', 'show_search', 'weather_df']:
        st.session_state[key] = None if key != 'show_search' else True

def setup_sidebar_location():
    """Sidebar for location search/management."""
    init_session_state()
    with st.sidebar:
        st.header("📍 Location")
        if st.session_state.show_search:
            with st.form("location_search", border=False):
                city_query = st.text_input(
                    "🔍 Search for a city",
                    value=st.session_state.current_location or "Bergen, Norway",
                    placeholder="e.g., Bergen, Norway"
                ).strip()

                submitted = st.form_submit_button(
                    "Get Weather",
                    use_container_width=True
                )

            if submitted and city_query:
                with st.spinner("Finding location..."):
                    result = geocode_city(city_query)

                    if result:
                        lat, lon, display_name = result
                        st.session_state.current_location = display_name
                        st.session_state.current_coords = (lat, lon)
                        st.session_state.show_search = False
                        st.session_state.weather_df = add_icons_to_weather_data(lat, lon)
                        st.rerun()
                    else:
                        st.error("Location not found. Try adding a country.")
                        
            elif submitted:
                st.warning("Please enter a city.")
        elif st.session_state.current_location:
            st.info(st.session_state.current_location)
            if st.button("🔍 Change Location", use_container_width=True):
                reset_location()
                st.rerun()
        else:
            reset_location()
            st.rerun()

def render_if_location_set(display_func):
    """If location is set, call display_func with weather_df."""
    if not (st.session_state.current_coords and not st.session_state.show_search):
        st.markdown("""
        Wearther replaces traditional weather icons with clothing recommendations.

        Use the sidebar to search for any city to see what you should wear today and over the coming week.
        """)
        st.info("👈 Search for a city in the sidebar to get started!")
        return
    df = st.session_state.weather_df
    if df is None or df.empty:
        st.warning("No weather data available.")
        return
    display_func(df)

def render_icon_help(df):
    icons_present = get_icons_from_df(df)

    with st.expander("What do these icons mean?"):
        display_icon_legend(icons_present, icon_size=30)

def render_footer():
    """Footer."""
    st.markdown("---")
    st.markdown("Data from [MET Norway](https://api.met.no/weatherapi/locationforecast/2.0/documentation) | Geocoding via [Nominatim](https://nominatim.org/) | Icons from [SVGrepo.com](https://www.svgrepo.com/)")

import streamlit as st
import os
import streamlit as st
from datetime import datetime, timedelta
from collections import defaultdict
from utils.config import CATEGORY_ORDER
from utils.config import ICON_CATEGORIES
from utils.icon_mapping import group_similar_hours, get_ordered_icons

def display_icons(categories, category_widths=None):
    """Render icons as images using their category as folder."""
    icon_to_category = {}
    for cat, icons in categories.items():
        for icon in icons:
            icon_to_category[icon] = cat

    base_path = "icons/"
    icon_paths = []
    for icon in get_ordered_icons(categories, category_widths):
        if icon == "spacer":
            path = os.path.join(base_path, "spacer.svg")
        else:
            filename = f"{icon}-svgrepo-com.svg"
            path = os.path.join(base_path, icon_to_category.get(icon), filename)
        if os.path.exists(path):
            icon_paths.append(path)
    if icon_paths:
        st.image(icon_paths, width=30)
    else:
        st.write("No specific items needed.")

def display_icon_legend(icons_present=None, icon_size=50):
    for category, icons in ICON_CATEGORIES.items():
        # Filter icons if icons_present is provided
        if icons_present is not None:
            filtered_icons = [(icon, label) for icon, label in icons if icon in icons_present]
            if not filtered_icons:
                continue
        else:
            filtered_icons = icons

        st.subheader(category) if icons_present is None else st.write(f"**{category}**")
        cols = st.columns(len(filtered_icons))
        for i, (icon, label) in enumerate(filtered_icons):
            icon_path = os.path.join("icons", category.lower(), f"{icon}-svgrepo-com.svg")
            cols[i].image(icon_path, width=icon_size)
            cols[i].caption(label)

def get_icons_from_df(df):
    icons_present = set()
    for categories in df['categories']:
        for cat, icons in categories.items():
            icons_present.update(icons)
    return icons_present

def get_category_widths(day_df):
    """Maximum number of icons per category for this day."""
    return {
        cat: max(len(cats.get(cat, [])) for cats in day_df["categories"])
        for cat in CATEGORY_ORDER
    }

def display_hourly_forecast(day_df):
    """Display grouped hourly forecast for a day."""
    category_widths = get_category_widths(day_df)

    for group in group_similar_hours(day_df):
        if not group:
            continue

        start, end = min(group), max(group)
        time_label = f"**{day_df.iloc[start]['local_time_short'][:2]}-{int(day_df.iloc[end]['local_time_short'][:2])+1:02d}**"

        col_left, col_right = st.columns([1, 3])
        col_left.markdown(time_label)

        with col_right:
            display_icons(day_df.iloc[start]["categories"], category_widths)

def display_daily_packing(day_df):
    """Display union of icons for a day's packing list."""
    union = defaultdict(set)
    for row in day_df['categories']:
        for cat, icons in row.items():
            union[cat].update(icons)
    display_icons({cat: list(union[cat]) for cat in CATEGORY_ORDER})

def display_today_forecast(df, with_selectbox=False):
    today_df = df[df['day_offset'] == 0]
    if today_df.empty:
        st.info("No data for today yet. Check back later.")
        return

    st.subheader(f"{today_df['day_name'].iloc[0]}, {today_df['date_display'].iloc[0]}")

    if not with_selectbox:
        display_hourly_forecast(today_df)
        return today_df

    # Only show future forecast times
    local_tz = today_df['datetime_local'].dt.tz
    now = datetime.now(local_tz)
    future_df = today_df[today_df['datetime_local'] >= now]
    if future_df.empty:
        st.info("No more forecast for today.")
        return

    future_end_times = future_df['datetime_local'] + timedelta(hours=1)
    labels = future_end_times.dt.strftime("%H:%M").replace("00:00", "24:00")
    label_to_endtime = dict(zip(labels, future_end_times))

    default_index = len(label_to_endtime) - 1

    selected_label = st.selectbox(
        "I'll be home at:",
        options=list(label_to_endtime.keys()),
        index=default_index
    )
    selected_end_time = label_to_endtime[selected_label]

    filtered_df = future_df[
        future_df['datetime_local'] + timedelta(hours=1) <= selected_end_time
    ]

    display_hourly_forecast(filtered_df)
    return filtered_df

def render_day_expanders(df, render_day_callable):
    """Render a sequence of day expanders for a dataframe."""
    if df.empty:
        st.info("No forecast days available.")
        return
    days = df.groupby('local_date').first().sort_values('day_offset').reset_index()
    for _, day_row in days.iterrows():
        title = f"{day_row['day_name']}, {day_row['date_display']}"
        day_df = df[df['local_date'] == day_row['local_date']]
        with st.expander(title, expanded=st.session_state.get('expand_all', False)):
            st.info("No detailed forecast data for this day.") if day_df.empty else render_day_callable(day_df)

def render_expand_button():
    """Expand/Collapse All button."""
    label = "Expand All" if not st.session_state.get('expand_all', False) else "Collapse All"
    if st.button(label):
        st.session_state['expand_all'] = not st.session_state.get('expand_all', False)
        st.rerun()
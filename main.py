# -*- coding: utf-8 -*-
"""
Created on Mon Oct 27 18:34:16 2025

@author: alice
"""

from time import sleep
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.express as px
import plotly.io as pio
import pydeck as pdk

from api import fetch_places
from insert_form import render_insert_form


def streamlit_app():
    """
    Launches the Streamlit web application for visualising and managing Japan trip locations.

    This function builds a two-tab Streamlit interface:
      • **Map tab** – Displays a dataframe of location pins and an interactive map
        (using Plotly Mapbox).
      • **DB Entry tab** – Provides a simple form for submitting new locations with
        attributes like name, description, importance, and geographic coordinates.

    The map uses a clean "carto-positron" style with pins sized and coloured
    according to their importance. Data is currently loaded from a static function
    (`read_pins()`), but the structure supports future integration with a database.

    Returns:
        None: The Streamlit app is executed directly and renders elements to the browser.
    """
    # Initial app setup
    st.title("🗾 Japan Trip Planner")
    tabs = st.tabs(["Map", "Add New Locations"])
    df_places = fetch_places()

    # Try to set plotly template based on app theme
    theme = st.get_option("theme.base")
    if theme == "dark":
        pio.templates.default = "plotly_dark"
        map_style = "carto-darkmatter"
    else:
        pio.templates.default = "plotly_white"
        map_style = "carto-positron"

    # Main landing page tab
    with tabs[0]:

        if df_places is not None and len(df_places.index) > 0:
            st.subheader("📍 Existing Destinations")
            st.dataframe(df_places)

            fig = px.scatter_map(
                df_places,
                lat="lat",
                lon="lon",
                hover_name="name",
                hover_data={"description": True, "importance": True},
                size="importance",
                color="importance",
                color_continuous_scale=px.colors.sequential.Plotly3,
                zoom=5,
                height=600,
                map_style=map_style,
                center={"lat": 36.2, "lon": 138.0},  # center on Japan
            )

            # Soft crimson pin styling
            fig.update_traces(marker=dict(size=16, opacity=0.9))

            # Minimalist map style and layout polish
            fig.update_layout(
                margin={"r": 0, "t": 0, "l": 0, "b": 0},  # remove border
                coloraxis_showscale=False,
                showlegend=False,
            )

            # Optional pastel background and borderless feel
            fig.update_layout(paper_bgcolor="#f8f9fa")

            st.plotly_chart(fig, use_container_width=True)

    # Tab containing form to create new rows
    with tabs[1]:
        render_insert_form()

if __name__ == "__main__":
    streamlit_app()

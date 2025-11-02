# -*- coding: utf-8 -*-
"""
Created on Mon Oct 27 18:34:16 2025

@author: alice
"""

import streamlit as st
import streamlit.components.v1 as components
import plotly.io as pio

from api import fetch_places
from components.insert_form import render_insert_form
from components.map import render_map


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
    df_places = fetch_places()

    # Main landing page tab
    if df_places is not None and len(df_places.index) > 0:
        
        # Section - Subheader and table
        st.subheader("Previously Saved Destinations")

        if st.button("➕ Add Destination"):
            render_insert_form()
        
        # Create top table to display all locations
        df_places["Delete"] = False
        st.dataframe(df_places)

        # Section - Map
        render_map(df_places)
        

if __name__ == "__main__":
    streamlit_app()

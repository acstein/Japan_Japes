# -*- coding: utf-8 -*-
"""
Created on Mon Oct 27 18:34:16 2025

@author: alice
"""

from time import sleep
import streamlit as st
import streamlit.components.v1 as components
import plotly.io as pio
import plotly.express as px
import pandas as pd

from api import delete_places, fetch_places, update_places
from components.insert_form import render_insert_form
from components.map import render_map
from utils import save_table_edits


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
    st.set_page_config(
        layout="wide", page_title="My Map App"  # Makes everything full width
    )

    # Main landing page tab
    if df_places is not None and len(df_places.index) > 0:

        # Section - Subheader and table
        st.subheader("Previously Saved Destinations")

        col1, col2, col3 = st.columns([1, 1, 5])

        with col1:
            if st.button("➕ Add Destination"):
                render_insert_form()
        
        with col2:
            button_placeholder = st.empty()

        # Create top table to display all locations
        df_places["delete"] = False
        df_edited = st.data_editor(df_places)

        # Detect changes for saving table edits
        rows_to_delete, rows_to_update = save_table_edits(df_places, df_edited)

        is_df_modified = bool(rows_to_delete or rows_to_update)

        with button_placeholder.container():
            if st.button("💾 Save Table Edits", disabled=not is_df_modified):
                if rows_to_delete:
                    delete_places(rows_to_delete)
                
                for item in rows_to_update:
                    update_places(item["place_id"], item["changes"])

                st.toast("Success!")
                st.cache_data.clear()
                st.rerun()

        # Section - Map
        render_map(df_places)


if __name__ == "__main__":
    streamlit_app()

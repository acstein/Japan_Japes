# -*- coding: utf-8 -*-
"""
Created on Mon Oct 27 18:34:16 2025

@author: alice
"""

from time import sleep
import streamlit as st
import pandas as pd
import plotly.express as px

from api import fetch_places, post_places

# st.set_page_config(page_title='Japan Japes', layout='wide')


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
    tabs = st.tabs(["Map", "DB Entry"])
    places = fetch_places()

    # Main landing page tab
    with tabs[0]:
        st.subheader("Map of Destinations")

        if places is not None and len(places.index) > 0:
            st.dataframe(places)

            fig = px.scatter_mapbox(
                places,
                lat="lat",
                lon="lon",
                hover_name="name",
                hover_data={"description": True, "importance": True},
                size="importance",
                color="importance",
                color_continuous_scale=px.colors.sequential.Plotly3,
                zoom=5,
                height=600,
            )

            # Soft crimson pin styling
            fig.update_traces(marker=dict(size=16, opacity=0.9))

            # Minimalist map style and layout polish
            fig.update_layout(
                mapbox_style="carto-positron",  # soft grayscale map tiles
                mapbox_center={"lat": 36.2, "lon": 138.0},  # center on Japan
                margin={"r": 0, "t": 0, "l": 0, "b": 0},  # remove boarder
                coloraxis_showscale=False,
                showlegend=False,
            )

            # Optional pastel background and borderless feel
            fig.update_layout(paper_bgcolor="#f8f9fa")

            st.plotly_chart(fig, use_container_width=True)

    # Tab containing form to create new rows
    with tabs[1]:
        st.header("Edit DB")

        # Form fields
        name = st.text_input("Name of Spot", value="Enter Name")
        desc = st.text_input("Description", value="Enter Description")
        link = st.text_input("Link", value="Enter URL")
        place_type = st.selectbox(
            "Place Type",
            ("Activity", "Location")
        )
        importance = st.number_input(
            "Rate Importance", min_value=0, max_value=10, value=5
        )
        submitter = st.selectbox("Submitter", ("George", "Alice"))
        lat = float(st.text_input("Enter latitude", value="0.0000"))
        lon = float(st.text_input("Enter longitude", value="0.0000"))

        # Form submission
        if st.button("Submit"):
            submitted = post_places(
                {
                    "name": name,
                    "description": desc,
                    "link": link,
                    "place_type": place_type,
                    "importance": importance,
                    "submitter": submitter,
                    "lat": lat,
                    "lon": lon,
                }
            )
            if submitted:
                st.text("Success!")
                st.rerun()  # reload the app to get the latest data


if __name__ == "__main__":
    streamlit_app()

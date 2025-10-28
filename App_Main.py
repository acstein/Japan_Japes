# -*- coding: utf-8 -*-
"""
Created on Mon Oct 27 18:34:16 2025

@author: alice
"""

import streamlit as st
import pandas as pd
import plotly.express as px

#st.set_page_config(page_title='Japan Japes', layout='wide')

def read_pins():
    data = {
        'name': ['Tokyo', 'Kyoto', 'Osaka'],
        'description': ['Capital city', 'Historic temples', 'Food paradise'],
        'importance': [10, 2, 9],
        'lat': [35.6762, 35.0116, 34.6937],
        'lon': [139.6503, 135.7681, 135.5023]
    }
    return pd.DataFrame(data)

def submit_runs(data):
    return True

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
    st.title('🗾 Japan Trip Planner')

    pins = read_pins()
    
    tabs = st.tabs(['Map', 'DB Entry'])

    with tabs[0]:
        st.subheader("Map of Destinations")
        
        st.dataframe(pins)
        
        fig = px.scatter_mapbox(
                pins,
                lat="lat",
                lon="lon",
                hover_name="name",
                hover_data={"description": True, "importance": True},
                size="importance",
                color="importance",
                color_continuous_scale=px.colors.sequential.Plotly3,
                zoom=5,
                height=600
            )

        # Soft crimson pin styling
        fig.update_traces(
            marker=dict(
                size=16,
                opacity=0.9
            )
        )
    
        # Minimalist map style and layout polish
        fig.update_layout(
            mapbox_style="carto-positron",  # soft grayscale map tiles
            mapbox_center={"lat": 36.2, "lon": 138.0},  # center on Japan
            margin={"r":0,"t":0,"l":0,"b":0}, # remove boarder
            #coloraxis_showscale=False,
            showlegend=False
        )
    
        # Optional pastel background and borderless feel
        fig.update_layout(paper_bgcolor="#f8f9fa")
    
        st.plotly_chart(fig, use_container_width=True)

    with tabs[1]:
        st.header('Edit DB')
        
        name = st.text_input('Name of Spot', value='Enter Name')
        desc = st.text_input('Description', value='Enter Description')
        importance = st.number_input('Rate Importance', min_value=0, max_value=10, value=5)
        submitter = st.text_input('Who are you???', value='Tell me')
        lat = float(st.text_input('Enter latitude', value='0.0000'))
        lon = float(st.text_input('Enter longitude', value='0.0000'))
        
        if st.button('Submit'):
            submitted = submit_runs([name, desc, importance, submitter, lat, lon])
            if submitted:
                st.text('Success!')

if __name__ == '__main__':
    streamlit_app()
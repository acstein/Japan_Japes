import plotly.express as px
import streamlit as st


def get_map_theme():
    theme = st.get_option("theme.base")
    if theme == "dark":
        return "carto-darkmatter"
    else:
        return "carto-positron"


def render_map(df):
    map_style = get_map_theme()
    fig = px.scatter_map(
        df,
        lat="lat",
        lon="lon",
        hover_name="name",
        hover_data=["description", "importance"],
        color="importance",
        color_continuous_scale=px.colors.sequential.Plotly3,
        zoom=5,
        height=600,
        map_style=map_style,
        center={"lat": 36.2, "lon": 138.0},  # center on Japan
    )

    # Soft crimson pin styling
    fig.update_traces(marker=dict(size=8, opacity=0.9), hoverinfo="text")

    # Minimalist map style and layout polish
    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},  # remove border
        coloraxis_showscale=False,
        showlegend=False,
    )

    st.plotly_chart(fig, use_container_width=True)

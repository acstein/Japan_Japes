import streamlit as st
import pandas as pd


def render_table(df_places: pd.DataFrame) -> pd.DataFrame:
    df_edited = st.data_editor(
        df_places,
        column_order=[
            "name",
            "description",
            "place_type",
            "nearest_city",
            "importance",
            "link",
            "submitter",
            "created_at",
            "visited",
            "delete",
        ],
        column_config={
            "name": st.column_config.TextColumn("Name", required=True),
            "description": st.column_config.TextColumn("Description", required=True),
            "place_type": st.column_config.SelectboxColumn(
                "Place Type",
                options=["Activity", "Location", "Food", "Accomodation"],
                help="Category of location, for filtering.",
                required=True,
            ),
            "nearest_city": st.column_config.TextColumn("Nearest City", required=True),
            "importance": st.column_config.NumberColumn(
                "Importance", min_value=0, max_value=10, required=True
            ),
            "link": st.column_config.LinkColumn(
                "URL", help="A link for information on the entry.", required=True
            ),
            "submitter": st.column_config.SelectboxColumn(
                "Submitter", options=["George", "Alice"], required=True
            ),
            "created_at": st.column_config.DatetimeColumn("Created At", required=True),
            "visited": st.column_config.CheckboxColumn("Visited"),
            "delete": st.column_config.CheckboxColumn("Delete")
        },
        hide_index=True,
    )
    return df_edited

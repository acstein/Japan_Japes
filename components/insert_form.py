import streamlit as st
from api import post_places


def apply_form_validation(required_fields: dict) -> None:
    """
    Check fields for missing values.
    Args:
        fields: specific form fields to check for missing values.
    Returns:
        None, creates st.warning if required fields are empty.
    """
    missing = [
        label
        for label, value in required_fields.items()
        if not value or isinstance(value, str) and not value.strip()
    ]

    if missing:
        st.warning(f"Please fill out all of the required fields: {', '.join(missing)}")
        st.stop()


@st.dialog("Add Destination", width="medium")
def render_insert_form():
    # Form fields
    with st.form("insert_form", clear_on_submit=True):
        name = st.text_input("Name of Spot *", value="Enter Name")
        desc = st.text_input("Description *", value="Enter Description")
        place_type = st.selectbox(
            "Place Type", ("Activity", "Location", "Food", "Accomodation")
        )
        importance = st.number_input("Importance", min_value=0, max_value=10, value=5)
        link = st.text_input("Link *", value="Enter URL")
        nearest_city = st.text_input("Nearest City *", value="Enter Nearest City")
        lat_lon = st.text_input("Lat/Lon (Google Format) *", value="Enter Value")
        submitter = st.selectbox("Submitter", ("George", "Alice"))

        submitted = st.form_submit_button("Submit")

    # Form submission
    if submitted:
        apply_form_validation(
            {
                "Name": name,
                "Description": desc,
                "Link": link,
                "Lat/Lon": lat_lon,
                "Submitter": submitter,
            }
        )
        try:
            lat, lon = [float(coord) for coord in lat_lon.split(", ")]
        except ValueError as e:
            st.error(
                f"Could not convert lat/lon supplied into coordinates. Ensure format is 'lat, lon'. Error: {e}"
            )
            st.stop()
        submitted = post_places(
            {
                "name": name,
                "description": desc,
                "place_type": place_type,
                "importance": importance,
                "link": link,
                "nearest_city": nearest_city,
                "lat": lat, # type: ignore
                "lon": lon, # type: ignore
                "submitter": submitter,
            }
        )
        if submitted:
            st.text("Success!")
            st.cache_data.clear()  # clear the cache to ensure latest data retrieved
            st.rerun()  # reload the app to get the latest data

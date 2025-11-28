from typing import TypedDict
from enum import Enum

import pandas as pd
import streamlit as st
from supabase import create_client, Client


# --- Support Classes ---
class Submitter(Enum):
    GEORGE = "George"
    ALICE = "Alice"


class FormFields(TypedDict):
    name: str
    description: str
    link: str
    place_type: str
    importance: int
    submitter: str
    lat: float
    lon: float
    nearest_city: str


# --- Configuration ---
url: str | None = st.secrets["SUPABASE_URL"]
key: str | None = st.secrets["SUPABASE_KEY"]

# Raise error to user if required environment variables are not saved
if url is None:
    raise ValueError("No URL provided! Ensure Supabase url is saved in a .env file.")
elif key is None:
    raise ValueError(
        "No API key provided! Ensure Supabase api key is saved in a .env file."
    )

supabase: Client = create_client(url, key)


# --- API Functions ---
@st.cache_data(ttl=300)  # cache data for 5 minutes
def fetch_places() -> pd.DataFrame | None:
    response = supabase.table("Places").select("*").execute()

    if response is not None:
        return pd.DataFrame(response.data)
    return None


def post_places(form_fields: FormFields) -> bool:
    new_row = {**form_fields}
    response = supabase.table("Places").insert(new_row).execute()
    return len(response.data) > 0  # at least one row of data was added


def update_places(place_id: str, changes: dict) -> bool:
    print(place_id, changes)
    response = supabase.table("Places").update(changes).eq("place_id", place_id).execute()
    if len(response.data) > 0:
        return True  # delete completed successfully
    else:
        return False  # delete failed


def delete_places(place_ids: list[str]) -> bool:
    response = supabase.table("Places").delete().in_("place_id", place_ids).execute()
    if len(response.data) > 0:
        return True  # delete completed successfully
    else:
        return False  # delete failed


if __name__ == "__main__":
    fetch_places()

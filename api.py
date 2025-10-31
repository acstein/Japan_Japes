import os
from dotenv import load_dotenv
from typing import TypedDict
from enum import Enum
from hashlib import sha256

import pandas as pd
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


# --- Configuration ---
load_dotenv()
url: str | None = os.environ.get("SUPABASE_URL")
key: str | None = os.environ.get("SUPABASE_KEY")

# Raise error to user if required environment variables are not saved
if (url is None):
    raise ValueError("No URL provided! Ensure Supabase url is saved in a .env file.")
elif (key is None):
    raise ValueError("No API key provided! Ensure Supabase api key is saved in a .env file.")

supabase: Client = create_client(url, key)


# --- API Functions ---
def fetch_places() -> pd.DataFrame | None:
    response = supabase.table("Places").select("*").execute()

    if response is not None:
        return pd.DataFrame(response.data)
    return None

def post_places(form_fields: FormFields) -> bool:
    new_row = {**form_fields}
    response = supabase.table("Places").insert(new_row).execute()
    return len(response.data) > 0  # at least one row of data was added


# def update_places() -> bool:
#     response = (
#         supabase.table("Places").update({"name": "piano"}).eq("id", 1).execute()
#     )


# def delete_places(id: int) -> bool:
#     response = supabase.table("countries").delete().eq("id", 1).execute()


if __name__ == '__main__':

    fetch_places()
import os
from supabase import create_client, Client


# --- Configuration ---
url: str | None = os.environ.get("SUPABASE_URL")
key: str | None = os.environ.get("SUPABASE_KEY")
if (url and key):
    supabase: Client = create_client(url, key)


# --- API Functions ---
def fetch_places():
    response = supabase.table("Places").select("*").execute()
    return response


def post_places():
    response = supabase.table("Places").insert({"id": 1, "name": "Pluto"}).execute()


def update_places():
    response = (
        supabase.table("instruments").update({"name": "piano"}).eq("id", 1).execute()
    )


def delete_places():
    response = supabase.table("countries").delete().eq("id", 1).execute()

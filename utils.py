import numpy as np

def save_table_edits(df_places, df_edited) -> tuple:
    # Detect deletes
    rows_to_delete: list[str] = df_edited.loc[
        df_edited["delete"] == True, "place_id"
    ].tolist()

    # Only compare columns which are not delete or PK
    compare_cols = [
        col for col in df_places.columns if col not in ["delete", "place_id"]
    ]  # ignore delete flag

    # Dataframe widget can be reordered - need to ensure same ordering of rows
    orig = df_places.set_index("place_id")[compare_cols]
    edit = df_edited.set_index("place_id")[compare_cols]
    common_ids = orig.index.intersection(
        edit.index
    )  # only keep common rows (ignore new insertions)
    changed = orig.loc[common_ids].compare(edit.loc[common_ids])

    # Interate through changed rows and add differences to dict
    rows_to_update = []
    for row_id in changed.index.unique():
        changes = {}
        for col in changed.loc[row_id].index.get_level_values(0).unique():
            new_val = edit.loc[row_id, col]

            if isinstance(new_val, np.generic):
                new_val = new_val.item()  # call .item() to get Python native type (np.int64 cannot be passed to Supabase)
            changes[col] = new_val
        rows_to_update.append({"place_id": row_id, "changes": changes})

    return rows_to_delete, rows_to_update

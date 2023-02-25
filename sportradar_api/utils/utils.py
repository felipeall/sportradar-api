from typing import Optional

import pandas as pd


def remove_str(text: str, strings_to_remove: list) -> str:
    for string in strings_to_remove:
        text = text.replace(string, "")

    return text


def explode_column(
    df_to_explode: pd.DataFrame, col_to_explode: str, cols_to_keep: Optional[list] = None
) -> pd.DataFrame:
    df = df_to_explode.copy()
    if cols_to_keep:
        df = df.loc[:, cols_to_keep + [col_to_explode]]

    df = df.explode(col_to_explode)

    normalized = pd.json_normalize(df[col_to_explode]).add_prefix(f"{col_to_explode}.")
    normalized.index = df.index

    df = pd.concat([df, normalized], axis=1)
    df = df.drop(columns=col_to_explode)

    return df


def remove_cols_str(df: pd.DataFrame, str_list: list) -> pd.DataFrame:
    df.columns = [remove_str(col, str_list) for col in df.columns]
    return df

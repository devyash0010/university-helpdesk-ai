
import pandas as pd
import json

def load_data(path="knowledge_base.csv"):
    df = pd.read_csv(path)
    return df

def get_categories(df):
    return list(df["label"])

def get_subcategories(df, category):
    row = df[df["label"] == category].iloc[0]
    subs = json.loads(row["subcategories"])
    return subs

def get_response(df, category):
    row = df[df["label"] == category].iloc[0]
    templates = json.loads(row["templates"])
    return templates[0]["message"]

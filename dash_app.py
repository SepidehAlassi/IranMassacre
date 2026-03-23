# app.py
# Run: python app.py
# Open: http://127.0.0.1:8050

import os
import math
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# -----------------------
# Config
# -----------------------
DATA_DIR = "data"

PROV_COORDS_PATH = os.path.join(DATA_DIR, "province_coords.csv")
DEATHS_PATH = os.path.join(DATA_DIR, "massacre_data.csv")

COL_PROVINCE = "province"
COL_AGE = "age"
COL_IS_FEMALE = "isFemale"

# -----------------------
# Data utilities
# -----------------------
MISSING_TOKENS = {"nan": pd.NA, "none": pd.NA, "": pd.NA}

def norm_series(s: pd.Series) -> pd.Series:
    """Normalize strings for robust matching."""
    return (
        s.astype(str)
         .str.strip()
         .str.lower()
         .replace(MISSING_TOKENS)
    )

def load_deaths() -> pd.DataFrame:
    return pd.read_csv(DEATHS_PATH)

def load_province_coords() -> pd.DataFrame:
    prov_df = pd.read_csv(PROV_COORDS_PATH)
    prov_df["Latitude"] = pd.to_numeric(prov_df["Latitude"], errors="coerce")
    prov_df["Longitude"] = pd.to_numeric(prov_df["Longitude"], errors="coerce")
    prov_df["prov_norm"] = norm_series(prov_df["Name"])
    return prov_df

def normalize_is_female(s: pd.Series) -> pd.Series:
    """Return boolean Series (True = female)."""
    if s.dtype == bool:
        return s.fillna(False)

    return (
        s.astype(str).str.strip().str.lower()
         .map({"yes": True, "true": True, "1": True})
         .fillna(False)
    )

def province_aggregates(df_deaths: pd.DataFrame) -> pd.DataFrame:
    """Aggregate person-level deaths -> province-level metrics."""
    df = df_deaths.copy()
    df["prov_norm"] = norm_series(df[COL_PROVINCE])

    # female flag
    if COL_IS_FEMALE in df.columns:
        df["female"] = normalize_is_female(df[COL_IS_FEMALE])
    else:
        df["female"] = False

    # age numeric + age-group flags
    df[COL_AGE] = pd.to_numeric(df[COL_AGE], errors="coerce")
    df["children"] = df[COL_AGE].notna() & (df[COL_AGE] <= 10)
    df["teenager"] = df[COL_AGE].notna() & (df[COL_AGE] >= 11) & (df[COL_AGE] <= 18)
    df["young_adult"] = df[COL_AGE].notna() & (df[COL_AGE] > 18) & (df[COL_AGE] <= 30)

    agg = (
        df.groupby("prov_norm", dropna=False)
          .agg(
              deaths=("prov_norm", "size"),
              female=("female", "sum"),
              children=("children", "sum"),
              teenager=("teenager", "sum"),
              young_adult=("young_adult", "sum"),
          )
          .reset_index()
    )

    for c in ["deaths", "female", "children", "teenager", "young_adult"]:
        agg[c] = agg[c].fillna(0).astype(int)

    return agg

# -----------------------
# Plot builders
# -----------------------
HOVER_DATA = {
    "deaths": True,
    "female": True,
    "children": True,
    "teenager": True,
    "young_adult": True,
    "prov_norm": False,  # keep internal key hidden
    # NOTE: Latitude/Longitude intentionally omitted
}

def make_map_figure(plot_df: pd.DataFrame, size_scale: str):

    if size_scale == "log":
        plot_df = plot_df.copy()
        plot_df["deaths_size"] = plot_df["deaths"].apply(
            lambda x: 0.0 if x <= 0 else math.log1p(x)
        )
        size_col, size_max = "deaths_size", 40
    else:
        size_col, size_max = "deaths", 40

    fig = px.scatter_mapbox(
        plot_df,
        lat="Latitude",
        lon="Longitude",
        size=size_col,
        size_max=size_max,
        hover_name="Name",
        zoom=4.2,
        center={"lat": 32.0, "lon": 53.0},
        height=650,
    )

    # ---- CUSTOM HOVER (removes lat/lon completely) ----
    fig.update_traces(
        hovertemplate=
        "<b>%{hovertext}</b><br><br>"
        "Total deaths: %{customdata[0]}<br>"
        "Female deaths: %{customdata[1]}<br>"
        "Children (≤10): %{customdata[2]}<br>"
        "Teenagers (11–18): %{customdata[3]}<br>"
        "Young adults (19–30): %{customdata[4]}"
        "<extra></extra>",
        customdata=plot_df[
            ["deaths", "female", "children", "teenager", "young_adult"]
        ].values
    )

    fig.update_layout(
        mapbox_style="open-street-map",
        title="Deaths by Province (centroid points)",
        margin=dict(l=10, r=10, t=50, b=10),
    )

    return fig

def make_age_pie(df_deaths: pd.DataFrame, bins: list[int] | None) -> px.pie:
    df = df_deaths.copy()
    df[COL_AGE] = pd.to_numeric(df[COL_AGE], errors="coerce")

    # use provided cuts only if valid, otherwise fall back
    default_cuts = [10, 18, 30, 40]

    if not bins or len(bins) != 4:
        cuts = default_cuts
    else:
        cuts = sorted(set(int(b) for b in bins))
        if len(cuts) != 4:
            cuts = default_cuts

    cut_bins = [-float("inf")] + cuts + [float("inf")]
    labels = [
        f"<{cuts[0]}",
        f"{cuts[0]}-{cuts[1]}",
        f"{cuts[1]}-{cuts[2]}",
        f"{cuts[2]}-{cuts[3]}",
        f">{cuts[3]}",
    ]

    df["age_group"] = pd.cut(
        df[COL_AGE],
        bins=cut_bins,
        labels=labels,
        right=False,   # <10, 10-18, 18-30, 30-40, >40
    )

    df["age_group"] = df["age_group"].astype(object)
    df.loc[df[COL_AGE].isna(), "age_group"] = "Unknown"

    counts = (
        df["age_group"]
        .value_counts(dropna=False)
        .reindex(labels + ["Unknown"], fill_value=0)
        .reset_index()
    )
    counts.columns = ["age_group", "count"]

    fig = px.pie(
        counts,
        names="age_group",
        values="count",
        title="Age Distribution",
    )

    fig.update_layout(margin=dict(l=10, r=10, t=50, b=10))
    return fig
# -----------------------
# Initial load (slider bounds)
# -----------------------
df0 = load_deaths()
max_slider = int(df0[COL_PROVINCE].notna().sum()) if len(df0) else 0

# -----------------------
# Dash app
# -----------------------
app = Dash(__name__)
app.title = "Deaths by Province"

app.layout = html.Div(
    style={"maxWidth": "1100px", "margin": "0 auto", "fontFamily": "system-ui, sans-serif"},
    children=[
        html.H1("Iran Massacre 2026 Statistics"),
        html.H2("Deaths by Province (centroid points)"),

        html.Div(
            style={"display": "flex", "gap": "16px", "alignItems": "center", "flexWrap": "wrap"},
            children=[
                html.Div(
                    style={"minWidth": "260px"},
                    children=[
                        html.Label("Minimum deaths (filter provinces)"),
                        dcc.Slider(
                            id="min_deaths",
                            min=0,
                            max=max_slider,
                            step=1,
                            value=0,
                            tooltip={"placement": "bottom", "always_visible": False},
                        ),
                    ],
                ),
                html.Div(
                    style={"minWidth": "220px"},
                    children=[
                        html.Label("Size scaling"),
                        dcc.Dropdown(
                            id="size_scale",
                            options=[
                                {"label": "Linear", "value": "linear"},
                                {"label": "Log (better for wide ranges)", "value": "log"},
                            ],
                            value="linear",
                            clearable=False,
                        ),
                    ],
                ),
                html.Button("Reload data", id="reload", n_clicks=0),
            ],
        ),

        dcc.Graph(id="map"),

        html.Hr(),
        html.H3("Age Distribution"),
        html.Label("Adjust Age Group Cutoffs"),
        dcc.RangeSlider(
            id="age_bins",
            min=0,
            max=80,
            step=1,
            value=[9, 18, 30],
            allowCross=False,
            marks={0: "0", 10: "10", 20: "20", 30: "30", 40: "40", 50: "50", 60: "60", 70: "70", 80: "80"},
        ),
        dcc.Graph(id="age_pie"),
        html.Hr(),
        html.H3("Deaths per Date"),
        dcc.Graph(id="date_bar"),
        html.Hr(),
        html.H3("Gender Distribution"),
        dcc.Graph(id="gender_pie"),

        html.Hr(),
        html.H3("Number of Deaths per Province"),
        dcc.Graph(id="province_bar"),

        html.Hr(),
        html.H3("Age Distribution by Province (Box Plot)"),

        html.Label("Choose province"),
        dcc.Dropdown(
            id="province_select",
            options=[],          # we will fill via callback
            value=None,
            clearable=True,
            placeholder="Select a province…",
        ),

        dcc.Graph(id="province_age_box"),

    ],
)

# -----------------------
# Callbacks
# -----------------------
@app.callback(
    Output("map", "figure"),
    Input("min_deaths", "value"),
    Input("size_scale", "value"),
    Input("reload", "n_clicks"),
)
def update_map(min_deaths, size_scale, _n_clicks):
    df_deaths = load_deaths()
    prov_df = load_province_coords()
    agg = province_aggregates(df_deaths)

    plot_df = prov_df.merge(agg, on="prov_norm", how="left")
    for c in ["deaths", "female", "children", "teenager", "young_adult"]:
        plot_df[c] = plot_df[c].fillna(0).astype(int)

    plot_df = plot_df[plot_df["deaths"] >= int(min_deaths)].copy()

    fig = make_map_figure(plot_df, size_scale)
    return fig

@app.callback(
    Output("age_pie", "figure"),
    Input("age_bins", "value"),
    Input("reload", "n_clicks"),
)
def update_age_pie(bins, _n_clicks):
    df_deaths = load_deaths()
    return make_age_pie(df_deaths, bins)
@app.callback(
    Output("gender_pie", "figure"),
    Input("reload", "n_clicks"),
)
def update_gender_pie(_n_clicks):

    df = load_deaths()

    # Normalize isFemale to boolean
    if "isFemale" in df.columns:
        df["isFemale"] = (
            df["isFemale"]
            .astype(str)
            .str.strip()
            .str.lower()
            .map({"yes": True, "true": True, "1": True})
            .fillna(False)
        )
    else:
        df["isFemale"] = False

    # Count
    counts = df["isFemale"].value_counts().sort_index()

    # Ensure both categories exist
    male_count = counts.get(False, 0)
    female_count = counts.get(True, 0)

    pie_df = pd.DataFrame({
        "Gender": ["Male", "Female"],
        "Count": [male_count, female_count]
    })

    fig = px.pie(
        pie_df,
        names="Gender",
        values="Count"
    )

    fig.update_layout(margin=dict(l=10, r=10, t=50, b=10))

    return fig
@app.callback(
    Output("province_select", "options"),
    Output("province_select", "value"),
    Input("reload", "n_clicks"),
)
def populate_province_dropdown(_n_clicks):
    df = load_deaths()
    provs = (
        df["province"]
        .dropna()
        .astype(str)
        .str.strip()
        .sort_values()
        .unique()
        .tolist()
    )

    options = [{"label": p, "value": p} for p in provs]
    default_value = provs[0] if provs else None
    return options, default_value

@app.callback(
    Output("province_age_box", "figure"),
    Input("province_select", "value"),
    Input("reload", "n_clicks"),
)
def update_province_age_box(selected_province, _n_clicks):
    df = load_deaths()

    # clean
    df["province"] = df["province"].astype(str).str.strip()
    df["age"] = pd.to_numeric(df["age"], errors="coerce")

    if not selected_province:
        # empty state (no province chosen)
        empty = px.box(title="Select a province to see age distribution")
        empty.update_layout(margin=dict(l=10, r=10, t=50, b=10))
        return empty

    sub = df[df["province"] == selected_province].copy()
    sub = sub[sub["age"].notna()]

    if sub.empty:
        empty = px.box(title=f"No valid age data for {selected_province}")
        empty.update_layout(margin=dict(l=10, r=10, t=50, b=10))
        return empty

    fig = px.box(
        sub,
        y="age",
        points="outliers",  # shows outliers
        title=f"Age Distribution — {selected_province}",
    )
    fig.update_layout(margin=dict(l=10, r=10, t=50, b=10))
    fig.update_yaxes(title="Age")
    return fig
@app.callback(
    Output("province_bar", "figure"),
    Input("reload", "n_clicks"),
)
def update_province_bar(_n_clicks):

    df = load_deaths()

    # Clean province column
    df["province"] = (
        df["province"]
        .astype(str)
        .str.strip()
        .replace({"nan": None, "": None})
    )

    counts = (
        df["province"]
        .value_counts(dropna=False)
        .reset_index()
    )

    counts.columns = ["Province", "Count"]

    fig = px.bar(
        counts,
        x="Province",
        y="Count",
        title="Number of Deaths per Province",
    )

    fig.update_layout(
        margin=dict(l=10, r=10, t=50, b=10),
        xaxis_tickangle=-90,
    )

    fig.update_xaxes(title="Province")
    fig.update_yaxes(title="Count")

    return fig
@app.callback(
    Output("date_bar", "figure"),
    Input("reload", "n_clicks"),
)
def update_date_bar(_n_clicks):

    df = load_deaths()

    # Ensure datetime format
    df["deathDate"] = pd.to_datetime(df["deathDate"], errors="coerce")

    # Drop invalid dates
    df = df[df["deathDate"].notna()]

    # Count deaths per date
    counts = (
        df["deathDate"]
        .value_counts()
        .sort_index()
        .reset_index()
    )

    counts.columns = ["deathDate", "count"]

    # Convert to string so every bar gets a tick
    counts["deathDate_str"] = counts["deathDate"].dt.strftime("%Y-%m-%d")

    fig = px.bar(
        counts,
        x="deathDate_str",
        y="count",
        text="count"
    )

    fig.update_layout(
        margin=dict(l=10, r=10, t=50, b=10),
    )

    fig.update_traces(textposition="outside")

    fig.update_xaxes(
        title="Date",
        type="category",                 # ensures every bar has a tick
        categoryorder="array",
        categoryarray=counts["deathDate_str"],   # preserve chronological order
        tickangle=-45
    )

    fig.update_yaxes(title="Count")

    return fig
# -----------------------
# Main
# -----------------------
if __name__ == "__main__":
    app.run(debug=True)
